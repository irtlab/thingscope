from thingscope_api import ThingScopeAPI

thingscope_api = ThingScopeAPI()

def insert_in_db(data_to_insert):
    # Insert a new device schema.
    inserted_dev = thingscope_api.insert(data_to_insert)
    return inserted_dev['_id'], inserted_dev

def get_devices_from_db():
    return thingscope_api.get_devices()

def update_in_db(inserted_dev_id, data_to_update):
    # Update the device data
    updated_dev = thingscope_api.update(inserted_dev_id, data_to_update)
    return updated_dev
    
def api_sign_out():
    # This is for authentication sign out at the end of your program.
    thingscope_api.sign_out()