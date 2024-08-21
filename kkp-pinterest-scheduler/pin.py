
from pinterest.organic.pins import Pin

def save_pin(board_id):
    pin_create = Pin.create(
        board_id=board_id,
        title="My Pin",
        description="Pin Description",
        media_source={
            "source_type": "image_url",
            "content_type": "image/jpeg",
            "data": "string",
            'url':'https://i.pinimg.com/564x/28/75/e9/2875e94f8055227e72d514b837adb271.jpg'
            },
    )
    print("Pin Id: %s, Pin Title:%s" %(pin_create.id, pin_create.title))