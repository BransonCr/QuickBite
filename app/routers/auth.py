
@router.post("/register", response_model=UserPublic, status_code=201)
async def register(user: UserCreate, userService: UserService = Depends()):
    return userService.create_user(user)
