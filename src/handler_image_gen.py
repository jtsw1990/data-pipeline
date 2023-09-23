'''Script to interact with DALL-E API.'''


def generate_image(event, context) -> None:
    '''Uses a placeholder string.

    Assumes that some JSON response is returned with 
    a link to where the image is hosted.
    )
    '''
    message = event['Records'][0]['Sns']['Message']
    print(f'Received SNS message: {message}')
    print('generate_image invoked')

    return None
