import uvicorn

import configs


if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host='0.0.0.0',
        port=8000,
        reload=configs.IS_DEBUG,
        loop='uvloop',
    )
