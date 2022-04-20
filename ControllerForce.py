import Sofa
import Sofa.Core
import Sofa.constants.Key as Key


class ControllerForce(Sofa.Core.Controller):

    def __init__(self, *a, **kw):
        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.name='ControllerForce'
        
        self.arm = kw["node"]
        self.cable_1 = self.arm.getChild('cable_1')
        self.cable_2 = self.arm.getChild('cable_2')
        self.cable_3 = self.arm.getChild('cable_3')
        self.cable_4 = self.arm.getChild('cable_4')

        self.force_1 = 0
        self.force_2 = 0
        self.force_3 = 0
        self.force_4 = 0


    def onKeypressedEvent(self, e):
        inputvalue_c1 = self.cable_1.aCable_1.value
        inputvalue_c2 = self.cable_2.aCable_2.value
        inputvalue_c3 = self.cable_3.aCable_3.value
        inputvalue_c4 = self.cable_4.aCable_4.value
        

        if e["key"] == Key.KP_1:
            self.force_1 = inputvalue_c1.value[0] + 100.0
        elif e["key"] == Key.Q:
            self.force_1 = inputvalue_c1.value[0] - 100.0
            if self.force_1 < 0:
                print(self.force_1)
                self.force_1 = 0

        if e['key'] == Key.KP_2:
            self.force_2 = inputvalue_c2.value[0] + 100.0
        elif e['key'] == Key.W:
            self.force_2 = inputvalue_c2.value[0] - 100.0
            if self.force_2 < 0:
                print(self.force_2)
                self.force_2 = 0

        if e['key'] == Key.KP_3:
            self.force_3 = inputvalue_c3.value[0] + 100.0
        elif e['key'] == Key.E:
            self.force_3 = inputvalue_c3.value[0] - 100.0
            if self.force_3 < 0:
                print(self.force_3)
                self.force_3 = 0

        if e['key'] == Key.KP_4:
            self.force_4 = inputvalue_c4.value[0] + 100.0
        elif e['key'] == Key.W:
            self.force_4 = inputvalue_c4.value[0] - 100.0
            if self.force_4 < 0:
                print(self.force_4)
                self.force_4 = 0

        inputvalue_c1.value = [self.force_1]
        inputvalue_c2.value = [self.force_2]
        inputvalue_c3.value = [self.force_3]
        inputvalue_c4.value = [self.force_4]
        return
