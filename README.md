# Dreamin_server
### 현재 개발중인 단계입니다.

## 개발 스택
### Back-end <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/>
### Database <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=PostgreSQL&logoColor=white"/> 
### IDE tools <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/VSCode-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/> 
### Deplpyment <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=Docker&logoColor=white"/> <img src="https://img.shields.io/badge/AWS EC2-232F3E?style=flat-square&logo=Amazon AWS&logoColor=white"/> <img src="https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=Gunicorn&logoColor=white"/> <img src="https://img.shields.io/badge/NGINX-009639?style=flat-square&logo=NGINX&logoColor=white"/>


## api 명세 관리
#### 클라이언트에서의 테스트 편리성을 위해 postman을 통해 관리
- <img src="./source/api document1.png" alt="api document">
- <img src="./source/api document2.png" alt="api document">
- <img src="./source/api document3.png" alt="api document">


## 트러블 슈팅
- 이미지 관련
  - 기존엔 form-data형식으로 이미지 파일 및 추가 요청 데이터를 받아 서버에서 이미지를 s3에 저장하는 방식이였습니다.
  - 하지만 여러개의 이미지 처리에서의 문제 및 다른 api과 비교했을때 image를 포함한 request는 json을 포함하지 않은 request는 form-data 혼용하게 되는 문제가 생겼습니다.
  - 결과적으로, 클라이언트에서의 요청전 image를 직접 s3에 저장후 서버로 이미지의 url을 전달해주는 방식으로 변경하였습니다.

## 실행 방법
- .env 파일 생성(우선 적으로 이뤄져야함)
~~~
SECRET_KEY='{django unique key}'
AWS_S3_ACCESS_KEY_ID='{엑세스 키 ID}'
AWS_S3_SECRET_ACCESS_KEY='{비밀 엑세스 키}'
AWS_STORAGE_BUCKET_NAME='{bucket_name}'
~~~
- 로컬 환경
~~~
$ git clone https://github.com/DreamIn-Developer/server.git
$ pip install requirements.txt
$ python manage.py migrate
$ python manage.py runserver
~~~

- 배포 환경
~~~
$ git clone https://github.com/DreamIn-Developer/server.git
root 위치에 nginx 하위 conf.d 생성
$ sudo docker-compose up -d
~~~

- nginx/conf.d
~~~
server {
        listen 80;
        server_name ~~;
        charset utf-8;

        error_log /var/log/nginx/error.log;

        location / {
                proxy_pass ~~;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static/ {
                autoindex on;
                alias /static/;
        }
}
~~~