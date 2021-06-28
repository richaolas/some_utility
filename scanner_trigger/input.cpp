#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
#include <string.h>  
#include <sys/types.h>  
#include <fcntl.h>  
#include <errno.h>  
#include <time.h>  
#include <linux/input.h>  
#include <string>
using namespace std;
 
int main()
{
	int keys_fd;
	char ret[2];
	struct input_event t;
	keys_fd = open("/dev/input/event15", O_RDONLY);
    printf("%d\n", keys_fd);
	if (keys_fd <= 0)
	{
		printf("open /dev/input/event15 device error!\n");
		return 0;
	}
    
	while (1)
	{
		if (read(keys_fd, &t, sizeof (t)) == sizeof (t))
		{
			if (t.type == EV_KEY)
			if (t.value == 0 || t.value == 1)
			{
				printf("key %d %s\n", t.code, (t.value) ? "Pressed" : "Released");
				if (t.code == KEY_ESC)
					break;
			}
		}
	}
 
	close(keys_fd);
 
	return 0;
}
