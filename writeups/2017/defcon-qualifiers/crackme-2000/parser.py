import sys

values = []
for line in sys.stdin:
    op, dummy, val = line.split(',')
    
    if val.find('ffffffffffffff') != -1:
        val = (256 - int(val.replace('ffffffffffffff', ''), 16)) * -1
    else:
        val = int(val, 16)
    
    if op == 'cmp':
        result = val
        for value in values:
            result = result + value
        sys.stdout.write(chr(result))
        
        values = []
    else:
        if op == 'add':
            val = val * -1
        
        values = values + [val]