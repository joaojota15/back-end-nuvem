from fastapi import APIRouter, Depends
from app.db.session import SessionLocal
from app.models import Post
from app.schemas import PostCreate, PostOut
from app.routers.users import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=PostOut)
def create_post(post_in: PostCreate, db = Depends(get_db), current_user = Depends(get_current_user)):
    post = Post(title=post_in.title, description=post_in.description, category=post_in.category, author_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return PostOut(id=str(post.id), title=post.title, description=post.description, category=post.category, author_id=str(post.author_id), created_at=post.created_at.isoformat())

@router.get('/recentes', response_model=list[PostOut])
def recent_posts(db = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(10).all()
    return [PostOut(id=str(p.id), title=p.title, description=p.description, category=p.category, author_id=str(p.author_id), created_at=p.created_at.isoformat()) for p in posts]