#!/usr/bin/env python
import sys
from beautifulhue.api import Bridge


def createConfig():
    created = False
    print 'Press the button on the Hue bridge'
    while not created:
        resource = {'user':{'devicetype': 'beautifulhuetest', 'name': username}}
        response = bridge.config.create(resource)['resource']
        if 'error' in response[0]:
            if response[0]['error']['type'] != 101:
                print 'Unhandled error creating configuration on the Hue'
                sys.exit(response)
        else:
            created = True


def getLightStatus(bridge, light_to_get):
    """
    Get the status of a light, such as brightness, etc.

    bridge       : a bridge object
    light_to_get : the number of the light to get.

    Returns : a dictionary of light information
    """
    try:
        return bridge.light.get({'which':light_to_get})['resource']['state']
    except Exception as e:
        return bridge.light.get({"which":int(light_to_get)})['resource']['state']



def updateLight(bridge, light_to_update, **kwargs):
    """
    Given a bridge and the number of a light, turn it off or on

    bridge          : the bridge that controls the light
    light_to_update : the number of the light to update

    Returns: nothing
    """

    current_light_status = getLightStatus(bridge, light_to_update)

    for k, v in kwargs['updates'].items():
        current_light_status[k] = kwargs['updates'][k]


    resource = {
    'which':light_to_update,
    'data':{
        'state':current_light_status
        }
    }

    bridge.light.update(resource)



def getSystemData(bridge):

    return bridge.config.get({'which':'system'})['resource']





def getLightNames(bridge):
    """

    Get the names and numbers of lights that the bridge knows about.



    bridge : a bridge object. use makeBridgeConnection() for this.


    Returns : a dictionary of light_name, light_number pairs.

    """


    lights = bridge.config.get({'which':'system'})['resource']['lights']


    light_dict = {lights[k]['name'] : k for (k,v) in lights.items()}


    return light_dict





def makeBridgeConnection(bridge_ip, username):
    """
    Given the ip of the bridge and a username to connect with
    return a bridge object.


    bridge_ip : the local ip of the bridge
    username  : username to connect to the bridge with.

    Returns : a bridge object.
    """


    return Bridge(device={'ip':'{0}'.format(bridge_ip)}, user={'name':username})

def main():

    bridge_ip = '10.0.0.37'
    username  = 'beautifulhuetest'

    bridge    = Bridge(device={'ip':'{0}'.format(bridge_ip)}, user={'name':username})

    systemData = getSystemData(bridge)


    if 'lights' in systemData:
        print 'Successfully connected to the Hub'
    elif 'error' in response[0]:
        error = response[0]['error']
        if error['type'] == 1:
            createConfig()
            main()

    lights = getLightNames(bridge)

    # light1_status = getLightStatus(bridge = bridge, light_to_get = lights['Piano'])

    # print light1_status

    updateLight(bridge = bridge, light_to_update = lights['Living room'],
        updates = {'on'    : False}
        )

    


if __name__ == '__main__':
    main()
