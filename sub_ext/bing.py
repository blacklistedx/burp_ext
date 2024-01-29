from burp import IBurpExtender                              #Typical burp extension import
from burp import IContextMenuFactory

from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib

API_KEY = 'API KEY'
API_HOST = 'api.bing.microsoft.com'                         #Create free microsfot account to get bing API key

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        callbacks.setExtensionName('Bing')
        callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem('Send to Bing', actionPerformed=self.bing_menu))
        return menu_list

    def bing_menu(self, event):
        http_traffic = self.context.getSelectedMessages()
        print('%d requests highlighted' % len(http_traffic))

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            print('User selected host: %s' % host)
            self.bing_search(host)
        return


    def bing_search(self, host):
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False

        if is_ip:
            ip_address = host
            domain = False
            
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        start_new_thread(self.bing_query, ('ip:%s' % ip_address,))
        if domain:
            start_new_thread(self.bing_query, ('domain:%s' % host,))

    def bing_query(self, bing_query_string):
        print('Performing Bing Search: %s' % bing_query_string)
