/*
 * Re: POPEN3:
 * This implementation of popen3() was created from scratch in June of 2011.  It
 * is less likely to leak file descriptors if an error occurs than the 2007
 * version and has been tested under valgrind.  It also differs from the 2007
 * version in its behavior if one of the file descriptor parameters is NULL.
 * Instead of closing the corresponding stream, it is left unmodified (typically
 * sharing the same terminal as the parent process).  It also lacks the
 * non-blocking option present in the 2007 version.
 *
 * No warranty of correctness, safety, performance, security, or usability is
 * given.  This implementation is released into the public domain, but if used
 * in an open source application, attribution would be appreciated.
 *
 * Mike Bourgeous
 * https://github.com/nitrogenlogic
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/wait.h>

#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>

#include "tui_popen.h"

/*
 * Sets the FD_CLOEXEC flag.  Returns 0 on success, -1 on error.
 */
static int set_cloexec(int fd)
{
	if(fcntl(fd, F_SETFD, fcntl(fd, F_GETFD) | FD_CLOEXEC) == -1) {
		perror("Error setting FD_CLOEXEC flag");
		return -1;
	}

	return 0;
}

/*
 * Runs command in another process, with full remote interaction capabilities.
 * Be aware that command is passed to sh -c, so shell expansion will occur.
 * Writing to *writefd will write to the command's stdin.  Reading from *readfd
 * will read from the command's stdout.  Reading from *errfd will read from the
 * command's stderr.  If NULL is passed for writefd, readfd, or errfd, then the
 * command's stdin, stdout, or stderr will not be changed.  Returns the child
 * PID on success, -1 on error.
 */
static pid_t popen3(const char *command, int *writefd, int *readfd, int *errfd)
{
	int in_pipe[2] = {-1, -1};
	int out_pipe[2] = {-1, -1};
	int err_pipe[2] = {-1, -1};
	pid_t pid;

	// 2011 implementation of popen3() by Mike Bourgeous
	// https://gist.github.com/1022231

	if(command == NULL) {
		fprintf(stderr, "Cannot popen3() a NULL command.\n");
		goto error;
	}

	if(writefd && pipe(in_pipe)) {
		perror("Error creating pipe for stdin");
		goto error;
	}
	if(readfd && pipe(out_pipe)) {
		perror("Error creating pipe for stdout");
		goto error;
	}
	if(errfd && pipe(err_pipe)) {
		perror("Error creating pipe for stderr");
		goto error;
	}

	pid = fork();
	switch(pid) {
		case -1:
			// Error
			perror("Error creating child process");
			goto error;

		case 0:
			// Child
			if(writefd) {
				close(in_pipe[1]);
				if(dup2(in_pipe[0], STDIN_FILENO) == -1) {
					perror("Error assigning stdin in child process");
					exit(-1);
				}
				close(in_pipe[0]);
			}
			else { // sparse allocation requirement makes this work
				close(STDIN_FILENO);
				if (-1 == open("/dev/null", O_RDONLY)){
					perror("Error disabling stdin in child process");
					exit(-1);
				}
			}

			if(readfd) {
				close(out_pipe[0]);
				if(dup2(out_pipe[1], STDOUT_FILENO) == -1) {
					perror("Error assigning stdout in child process");
					exit(-1);
				}
				close(out_pipe[1]);
			}
			else {
				close(STDOUT_FILENO);
				if (-1 == open("/dev/null", O_WRONLY)){
					perror("Error disabling stdout in child process");
					exit(-1);
				}
			}

			if(errfd) {
				close(err_pipe[0]);
				if(dup2(err_pipe[1], STDERR_FILENO) == -1) {
					perror("Error assigning stderr in child process");
					exit(-1);
				}
				close(err_pipe[1]);
			}
			else {
				close(STDERR_FILENO);
				if (-1 == open("/dev/null", O_WRONLY)){
					/* can't perror this one */
					exit(-1);
				}
			}

			execl("/bin/sh", "/bin/sh", "-c", command, (char *)NULL);
			perror("Error executing command in child process");
			exit(-1);

		default:
			// Parent
			break;
	}

	if(writefd) {
		close(in_pipe[0]);
		set_cloexec(in_pipe[1]);
		*writefd = in_pipe[1];
	}
	if(readfd) {
		close(out_pipe[1]);
		set_cloexec(out_pipe[0]);
		*readfd = out_pipe[0];
	}
	if(errfd) {
		close(err_pipe[1]);
		set_cloexec(out_pipe[0]);
		*errfd = err_pipe[0];
	}

	return pid;

error:
	if(in_pipe[0] >= 0) {
		close(in_pipe[0]);
	}
	if(in_pipe[1] >= 0) {
		close(in_pipe[1]);
	}
	if(out_pipe[0] >= 0) {
		close(out_pipe[0]);
	}
	if(out_pipe[1] >= 0) {
		close(out_pipe[1]);
	}
	if(err_pipe[0] >= 0) {
		close(err_pipe[0]);
	}
	if(err_pipe[1] >= 0) {
		close(err_pipe[1]);
	}

	return -1;
}

static void to_luafile(lua_State* L, int fd, const char* mode)
{
	if (-1 == fd){
		lua_pushnil(L);
		return;
	}

	FILE** pf = lua_newuserdata(L, sizeof(FILE*));
	*pf = fdopen(fd, mode);
	luaL_getmetatable(L, LUA_FILEHANDLE);
	lua_setmetatable(L, -2);
}

int tui_popen(lua_State* L)
{
	const char* command = luaL_checkstring(L, 1);
	const char* mode = luaL_optstring(L, 2, "rwe");

	int sin_fd = -1;
	int sout_fd = -1;
	int serr_fd = -1;

	int* sin = NULL;
	int* sout = NULL;
	int* serr = NULL;

	if (strchr(mode, (int)'r'))
		sout = &sout_fd;

	if (strchr(mode, (int)'w'))
		sin = &sin_fd;

	if (strchr(mode, (int)'e'))
		serr = &serr_fd;

/* need to also return the pid so that waitpid is possible */
	pid_t pid = popen3(command, sin, sout, serr);

	if (-1 == pid)
		return 0;

	to_luafile(L, sin_fd, "w");
	to_luafile(L, sout_fd, "r");
	to_luafile(L, serr_fd, "r");
	lua_pushnumber(L, pid);

	return 4;
}

int tui_pid_status(lua_State* L)
{
	pid_t pid = luaL_checkint(L, 1);
	int status;
	pid_t res = waitpid(pid, &status, WNOHANG);
	if (-1 == res){
		lua_pushboolean(L, 0);
		return 1;
	}

	if (status){
		if (WIFEXITED(status)){
			lua_pushboolean(L, 0);
			lua_pushnumber(L, WEXITSTATUS(status));
			return 2;
		}
	}

	lua_pushboolean(L, 1);
	return 1;
}
