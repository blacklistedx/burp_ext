#Burp extension to work with intruder creating custom generated payloads


from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList
import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callback = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.resisterIntruderPayloadGeneratorFactory(self)
        return

    def getGeneratorName(self):
        return 'Payload Generator'

    def createNewInstance(self, attack):
        return Fuzzer(self, attack)

#Create class for Fuzzer (intruder generator)

class Fuzzer(IIntruderPayloadGenerator):
    def __init__(self, entender, attack):
        self.extender = extender
        self.helpers = extender._helpers
        self.attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):
        #Convert byte array to string

        payload = ''.join(chr(x) for x in current_payload)
        payload = self.mutate_payload(payload)
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):
        # Pick a sample mutator or even call an external script
        picker = random.randint(1, 3)

        # Select a random offset in the payload to inject possible attacks below
        offset = random.randint(0, len(original_payload) - 1)
        front, back = original_payload[:offset], original_payload[offset:]

        # Random offset insert a SQL injection attempt

        if picker == 1:
            front += "'"

        # Jam an XSS attempt in as well testing in html context

        elif picker == 2:
            front += "<script>alert(1);</script>"

        # Repeat a random chunk of the original payload

        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]

        return fron + back
