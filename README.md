# Dreamin_server
## 순수예술인을 위한 포트폴리오 관리및 정보 공유 커뮤니티_서버

### 배포 및 기타사항
- AWS EC2환경에서 docker 컨테이너 기반 배포
- 이미지 및 정적 파일은 AWS S3를 통한 해결 예정
- 개발 DB는 SQLITE3, 배포 DB는 RDS의 POSTGRESQL환경에서 운영 예정
- SSL인증서의 경우, 현재는 certbot에서 발급받아 적용하였지만 최종 배포 단계에서 ACM을 통해 SSL인증서 이용예정
- 추가 사항은 개발을 진행하며 계속하여 업데이트

### API 요약
**소셜로그인을 통한 유저 가입 : POST /api/users/google or kakao**
- 클라이언트에서 넘겨준 소셜의 access_token을 통해 회원가입을 진행
- jwt 방식의 인증 처리

**유저의 목록을 조회 : GET /api/users**
- 메인페이지의 컨텐츠 중 하나인 유저의 목록을 조회합니다.

**유저 정보 조회 : GET /api/users/:pk**
- pk 값에 따른 유저의 정보를 조회합니다.
- 개인 프로필에 쓰입니다.

**유저 정보 수정 : PUT,PATCH /api/users/:pk**
- pk 값에 따른 유저의 정보를 수정 합니다.

**닉네임 중복 체크 : GET /api/users?nickname=~~**
- 파라미터로 전달받은 nickname 값의 중복 확인을 진행합니다.

**유저 팔로우 : POST /api/users/:pk/follow**
- 헤더의 토큰값 디코드와 pk값을 통해 유저끼리 팔로우를 진행합니다.

**유저 활동분야 조회 : GET /api/category/list**
- 회원가입폼에서 전달받을 유저의 활동분야 카테고리를 반환합니다.

**개인 피드 목록 조회 : GET /api/posts**
- 개인 프로필의 피드 부분에서 활용된 게시글 리스트를 반환합니다.

**개인 피드 생성 : POST /api/posts**
- 개인 피드글을 생성합니다.

**개인 피드 글 수정 : PUT, PATCH /api/posts/:pk**
- 해당 개인 피드글을 수정합니다.

**개인 피드 글 삭제 : DELETE /api/posts/:pk**
- 해당 개인 피드글을 삭제합니다.

**피드 글의 댓글 리스트 조회 : GET api/posts/:pk/comments**
- pk 값의 피드글에 대한 댓글 리스트를 반환합니다.

**피드 글 스크랩 : POST api/posts/:pk/scrap**
- pk 값의 피드글을 스크랩합니다.
- 헤더의 토큰 값에 대한 유저와 pk 값으로 진행합니다.

**팀 리스트 조회 : GET api/team**
- 메이페이지의 컨텐츠로 이용될 팀 전체 리스트를 조회합니다.

**팀 개별 조회 : GET api/team/:pk**
- pk 값에 따른 팀 정보를 조회합니다.

**팀 정보 수정 : PUT,PATCH api/team/:pk**
- pk 값에 따른 팀 정보를 수정합니다.

**팀 삭제 : DELETE api/team/:pk**
- pk 값에 따른 팀을 삭제합니다.
- 팀을 만든 리더만 삭제 가능하도록 퍼미션 부여 예정입니다.

**팀 즐겨찾기 : POST api/team/:pk**
- 헤더의 토큰 값과 pk 값을 통해 팀을 즐겨찾기 등록할수 있습니다.

**팀 지원 : POST api/team/:pk**
- 헤더의 토큰값에 해당하는 유저가 pk 값에 따른 팀에 지원할수 있습니다.

**팀원 조회 : GET api/team/:pk/members**
- pk 값에 해당하는 팀의 팀원을 조회합니다.
- member 모델의 member_type이 confirmed인 팀원 조회

**팀원 지원 목록 조회 : GET /api/team/pended_members**
- pk 값에 해당하는 팀에 지원한 유저를 조회합니다.
- member 모델의 member_type이 pended인 팀원 조회
- 팀의 리더만 볼수 있도록 퍼미션 부여 예정입니다.

**알림 관련 작업 진행중**
- 대부분 django_signal기능을 이용해 모델링중
- socket을 통한 구현이 아닌 클라이언측에서 유저의 특정 작업이 있을때 요청하도록 개발중
- 우리 서비스에서 알림이 즉각적으로 반응해야하는것이 필수라고 판단하지 않았기 때문에 socket을 통한 개발x

**팀 관련 피드글 작업 진행중**

**댓글 관련 작업 진행중**

