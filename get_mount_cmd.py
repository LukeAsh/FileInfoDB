"""
Create mount command for output from
{{{
sudo lvchange -ay wdmp
sudo lvchange -ay wde
# cd /dev/mapper
for i in `ls /dev/mapper -x1`; do sudo blkid /dev/mapper/$i >> in.txt; done
}}}
"""

def get_value(arg_value):
    """get value from ARG="value"
    """

    return arg_value[arg_value.find('"')+1:arg_value.rfind('"')]

with open('in.txt', 'r') as f:
    lines = f.readlines()

with open('out.txt', 'w') as f:
    for line in lines:
        # print(line)
        sl = line.split()
        l = get_value(sl[1])
        u = get_value(sl[2])
        d = sl[0][:-1]
        print('mkdir /media/{dir}'.format(dir=l))
        f.write('mkdir /media/{dir}\n'.format(dir=l))
        print('mount --uuid "{uuid}" /media/{label}'.format(dev_name=d, uuid=u, label=l))
        f.write('mount --uuid "{uuid}" /media/{label}\n'.format(dev_name=d, uuid=u, label=l))
