#include <linux/kernel.h>
#include <linux/module.h>

#include <linux/fs.h>
#include <linux/cdev.h>
#include <asm/uaccess.h>
#include <linux/uaccess.h>
#include <linux/ioctl.h>

MODULE_LICENSE("GPL");

MODULE_AUTHOR("th3f0x <stripathi1@cs.iitr.ac.in>");
MODULE_DESCRIPTION("like module");

#define SUCCESS 0
#define DEVICE_NAME "like"
#define MAJOR_NUMBER 489

#define IOCTL_CALL _IOWR(MAJOR_NUMBER,0,char *)

static int like_open(struct inode *inode, struct file *file) {
    printk("Device opened\n");
    return SUCCESS;
}

static int like_close(struct inode *inode, struct file * file) {
    printk("Device Closed\n");
    return SUCCESS;
}

struct comment {
    char *comment_string;
    unsigned long long *likes;
};

static long like_ioctl(struct file *file, unsigned int ioctl_num, unsigned
        long ioctl_parm) {
    struct comment c;
    switch(ioctl_num){
        case IOCTL_CALL:
            copy_from_user(&c, ioctl_parm, sizeof(struct comment));
            *c.likes += 1;
            return SUCCESS;
            break;
        default :
            break;
    }
    return SUCCESS;
  }

static struct file_operations like_fops = {
    .owner = THIS_MODULE,
    .read = 1,
    .open = like_open,
    .release = like_close,
    .unlocked_ioctl = like_ioctl,
};

int init_module(void) {
    int Major;
    Major = register_chrdev(MAJOR_NUMBER,DEVICE_NAME,&like_fops);
    if (Major < 0) {
        printk("Registering the character device failed with %d\n",
                Major);
        return Major;
    }
    return SUCCESS;
}

void cleanup_module(void) {
    unregister_chrdev(MAJOR_NUMBER,DEVICE_NAME);
}


