# Dreamin_server
## 순수예술인을 위한 포트폴리오 관리및 정보 공유 커뮤니티_서버

---

## Development Environments
### Back-end <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/>
### Database <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=PostgreSQL&logoColor=white"/> 
### IDE tools <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/VSCode-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/> 
### Deplpyment <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=Docker&logoColor=white"/> <img src="https://img.shields.io/badge/AWS EC2-232F3E?style=flat-square&logo=Amazon AWS&logoColor=white"/> <img src="https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=Gunicorn&logoColor=white"/> <img src="https://img.shields.io/badge/NGINX-009639?style=flat-square&logo=NGINX&logoColor=white"/>
- AWS EC2환경에서 docker 컨테이너 기반 배포
- 이미지 및 정적 파일은 AWS S3를 통한 해결 예정
- 개발 DB는 SQLITE3, 배포 DB는 RDS의 POSTGRESQL환경에서 운영 예정
- SSL인증서의 경우, 현재는 certbot에서 발급받아 적용하였지만 최종 배포 단계에서 ACM을 통해 SSL인증서 이용예정
- 추가 사항은 개발을 진행하며 계속하여 업데이트

