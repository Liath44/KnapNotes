import uvicorn

if __name__ == '__main__':
	uvicorn.run(
		'main:app',
		reload=True,
		ssl_keyfile="./ssl/private.key",
		ssl_certfile="./ssl/certificate.crt"
	)
