#!/usr/bin/env python
import json
import time
from harc.threading.Abort import Abort
from harc.threading.Threads import Threads
from harc.threading.Runner import Runner
from harc.executors.WatchWorker import WatchWorker
from harc.executors.QueueWatcher import QueueWatcher


def main():
    data = open("harc_message.json")
    settings = json.load(data)

    abort = Abort()
    threads = Threads(abort)
    t = Runner.run(WatchWorker(QueueWatcher(), settings, threads, abort))
    threads.append({'thread': t})

    try:
        while True:
            time.sleep(settings['agent_idle_delay'])
    except:
        threads.abort()


if __name__ == "__main__":
    main()


