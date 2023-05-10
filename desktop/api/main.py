import uvicorn

from src.app import app, const


def main():
    uvicorn.run(app=app, host=const.API_HOST, port=const.API_PORT)


if __name__ == '__main__':
    main()
