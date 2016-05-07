#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

static int module_init_function(void)
{
    printk(KERN_INFO "Prueba 1 init\n");
    return 0;
}

static void module_exit_function(void)
{
    printk(KERN_INFO "Prueba 1 fin\n");
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("marcelarosalesj");
MODULE_DESCRIPTION("Linux Kernel Module Test");

module_init(module_init_function);
module_exit(module_exit_function);
