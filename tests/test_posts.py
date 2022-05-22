from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200 

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")

    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.body == test_posts[0].body
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, body, published", [
    ("awesome new title", "awesome new content", True),
    ("Italian Pizaa", "I love sausages", True),
    ("tallest building in Yverdon", "I live there", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, body, published):
    res = authorized_client.post("/posts/", json={"title": title, "body":body, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title  
    assert created_post.body == body  
    assert created_post.published == published  
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_ture(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={"title": "random title", "body":"random content"})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "random title"
    assert created_post.body == "random content" 
    assert created_post.published == True 
    assert created_post.owner_id == test_user['id']

    
def test_unauthorized_user_create_posts(client, test_user, test_posts):
    
    res = client.post("/posts/", json={"title": "random title", "body":"random content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_posts(client, test_user, test_posts):
    
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user , test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204
    
def test_delete_post_non_exist(authorized_client, test_user , test_posts):
    res = authorized_client.delete(f"/posts/88800000")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user , test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_user , test_posts):
    data = {
        "title":"update title",
        "body":"updated body",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)