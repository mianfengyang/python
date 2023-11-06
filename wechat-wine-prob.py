#!/usr/bin/env python3

import psutil
# import time
import gi
gi.require_version('Wnck', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Wnck, Gtk

class WeChatWindowMonitor():
    def __init__(self):
        self.screen = Wnck.Screen.get_default()
        self.screen.force_update()

        self.wechat_window_name = "微信"
        self.wechat_process_name = "WeChat.exe"

        self.screen.connect("active_window_changed", self.active_window_changed)

    def __get_window_process_name(self, window):
        try:
            pid = window.get_pid()
            return psutil.Process(pid).name()
        except:
            pass
        return "window maybe closed"

    def active_window_changed(self, screen, window):
        active_window = self.screen.get_active_window()
        active_process_name = self.__get_window_process_name(active_window)
        # print("active process: " + active_process_name)
        if active_window and active_window.get_name() != self.wechat_window_name and self.wechat_process_name != active_process_name:
            # print("current window: " + active_window.get_name())
            for win in self.screen.get_windows():
                if win and win.get_name() == self.wechat_window_name:
                    # 我的情况是最小化微信窗口，透明框即消失，也可以采用参考文章的关闭。
                    # win.close(time.time())
                    win.minimize()

    def run(self):
        Gtk.main()

WeChatWindowMonitor().run()
