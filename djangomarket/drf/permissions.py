from rest_framework import permissions

class IsAuthorOrReadonly(permissions.BasePermission):
    # has_permission과 has_object_permission 함수 두개가 이미 구현되어있다.
    # 사용자는 이를 오버라이딩 하여 커스텀

    # 인증이 되어야먄 목록조회/포스팅 등록을 허용
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    # 
    def has_object_permission(self, request, view, obj):
        
        # print('obj.author', obj.author)
        '''
        SAFE_METHODS  = ["GET", "HEAD", "OPTIONS"]
        '''
        if request.method in permissions.SAFE_METHODS: #단순 조회용 요청이면..
            return True
        print("obj", type(obj))
        return obj.author == request.user #POST, PUT, DELETE 등의 요청은 글 작성자만 수정허용-