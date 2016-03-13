#!/usr/bin/env python
from __future__ import print_function

import sys

from beautifulhue.api import Bridge

class BridgeInterface():
    def __init__(self, bridge_ip, bridge_username):
        self.ip = bridge_ip
        self.username = bridge_username

        self.bridge = self.connect_to_bridge()

        if 'lights' in self.system_data():
            pass
        else:
            self.create_config()




        self.light_names = self.get_light_names()

    def connect_to_bridge(self):

        return Bridge(device={'ip':'{0}'.format(self.ip)},
                             user={'name':self.username})

    def system_data(self):

        data = self.bridge.config.get({'which':'system'})['resource']
        return data

    def create_config(self):


        created = False
        print('Press the button on the Hue bridge')
        while not created:
            resource = {'user':{'devicetype': 'beautifulhuetest', 'name': username}}
            response = self.bridge.config.create(resource)['resource']
            if 'error' in response[0]:
                if response[0]['error']['type'] != 101:
                    print('Unhandled error creating configuration on the Hue')
                    sys.exit(response)
            else:
                created = True


    def get_light_status(self, light_to_get):
        """
        Get the status of a light, such as brightness, etc.

        bridge       : a bridge object
        light_to_get : the number of the light to get.

        Returns : a dictionary of light information
        """
        try:
            return self.bridge.light.get({'which':light_to_get})['resource']['state']
        except Exception as e:
            return self.bridge.light.get({"which":int(light_to_get)})['resource']['state']



    def update_light(self, light_to_update, **kwargs):
        """
        Given a bridge and the number of a light, turn it off or on

        bridge          : the bridge that controls the light
        light_to_update : the number of the light to update

        Returns: nothing
        """

        current_light_status = self.get_light_status(light_to_update)

        for k, v in kwargs['updates'].items():
            current_light_status[k] = kwargs['updates'][k]


        resource = {
        'which':light_to_update,
        'data':{
            'state':current_light_status
            }
        }

        self.bridge.light.update(resource)

    def get_light_names(self):
        """
        Get the names and numbers of lights that the bridge knows about.
        bridge : a bridge object. use makeBridgeConnection() for this.

        Returns : a dictionary of light_name, light_number pairs.
        """

        lights = self.bridge.config.get({'which':'system'})['resource']['lights']
        light_dict = {lights[k]['name'] : k for (k,v) in lights.items()}

        return light_dict


def main():

    bi = BridgeInterface(bridge_ip = '10.0.0.37', bridge_username = 'beautifulhuetest')



    print(bi.light_names)

    bi.update_light(light_to_update = bi.light_names['Jim bed'],
        updates = {'on'    : False}
        )




if __name__ == '__main__':
    main()
