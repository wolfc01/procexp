from collections import Counter
import linecache
import os
import tracemalloc
import PyQt6.QtWidgets as QtWidgets 

tracemalloc.start()

def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

def do():
    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)

def count_items(mainUi):
    count = 0
    it = QtWidgets.QTreeWidgetItemIterator(mainUi.processTreeWidget)
    while it.value():
        item = it.value()
        if item.parent():
            if item.parent().isExpanded():
                count +=1
            else:
            # root item
                count += 1
        it += 1
    print(count)