from thingscope_api import ThingScopeAPI

thingscope_api = ThingScopeAPI()

# Insert a new device schema.
inserted _dev = thingscope_api.insert({'foo': 'bar'})

# Update the device data
#updated _dev = thingscope_api.update(inserted _dev['_id'], {'foo': 'bar1'})

devices = thingscope_api.get_devices()
print(devices)

# This is for authentication sign out at the end of your program.
thingscope_api.sign_out()
