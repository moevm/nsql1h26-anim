import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Header } from "@components/header";
import { PostCard, PostFilters, PostModal } from "@components/post";
import { HiOutlinePlus } from "react-icons/hi";
import { request } from '@api/axios';
import styles from './FeedPage.module.css';

const LIMIT = 5;

export const FeedPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [posts, setPosts] = useState([]);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  const filters = {
    search: searchParams.get('search') || '',
    sort: searchParams.get('sort') || 'newest',
    tag: searchParams.get('tag') || '',
    author: searchParams.get('author') || '',
    taxon: searchParams.get('taxon') || '',
    scientificName: searchParams.get('scientificName') || '',
    onlyFollowed: searchParams.get('onlyFollowed') === 'true',
    dateFrom: searchParams.get('dateFrom') || '',
    dateTo: searchParams.get('dateTo') || '',
  };

  const fetchPosts = useCallback(async (currentOffset = 0) => {
    setLoading(true);
    try {
      const cleanParams = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '' && v !== false)
      );
      const response = await request('GET', 'posts', {
        ...cleanParams,
        limit: LIMIT,
        offset: currentOffset
      });
      if (currentOffset === 0) {
        setPosts(response.items);
      } else {
        setPosts(prev => [...prev, ...response.items]);
      }
      setHasMore(response.hasMore);
    } catch (err) {
      console.error("Ошибка при загрузке постов:", err);
    } finally {
      setLoading(false);
    }
  }, [searchParams]);

  useEffect(() => {
    setOffset(0);
    fetchPosts(0);
  }, [searchParams, fetchPosts]);

  const handleLoadMore = () => {
    const nextOffset = offset + LIMIT;
    setOffset(nextOffset);
    fetchPosts(nextOffset);
  };

  const setFilter = (key, value) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (value) next.set(key, value);
      else next.delete(key);
      return next;
    }, { replace: true });
  };

  const handleCreatePost = async (payload) => {
    setActionLoading(true);
    try {
      await request('POST', 'posts', payload);
      setIsModalOpen(false);
      setOffset(0);
      fetchPosts(0);
    } catch (err) {
      alert(err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleLike = async (id) => {
    try {
      await request('POST', `posts/${id}/like`);
      setPosts(prev => prev.map(post =>
        post.id === id
          ? { ...post, isLiked: !post.isLiked, likesCount: post.isLiked ? post.likesCount - 1 : post.likesCount + 1 }
          : post
      ));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Удалить этот пост?")) return;
    try {
      await request('DELETE', `posts/${id}`);
      setPosts(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      alert("Ошибка при удалении");
    }
  };

  return (
    <div className={styles.feedWrapper}>
      <Header />
      <main className={styles.mainContent}>
        <header className={styles.feedHeader}>
          <div className={styles.headerInfo}>
            <h1>Лента активностей</h1>
            <p>Исследуйте мир дикой природы вместе с сообществом</p>
          </div>
          <div className={styles.headerActions}>
            <button className={styles.addBtn} onClick={() => setIsModalOpen(true)}>
              <HiOutlinePlus /> Создать пост
            </button>
          </div>
        </header>

        <PostFilters
          filters={filters}
          setFilter={setFilter}
          filtersOpen={filtersOpen}
          setFiltersOpen={setFiltersOpen}
          resetFilters={() => setSearchParams({})}
        />

        <div className={styles.postsGrid}>
          {posts.map(post => (
            <PostCard
              key={post.id}
              post={post}
              onLike={handleLike}
              onDelete={handleDelete}
            />
          ))}
        </div>

        {loading && <div className={styles.loader}>Загрузка...</div>}

        {!loading && posts.length === 0 && (
          <div className={styles.emptyState}>Постов пока нет. Будьте первым!</div>
        )}

        {!loading && hasMore && (
          <div className={styles.loadMoreWrapper}>
            <button className={styles.loadMoreBtn} onClick={handleLoadMore}>
              Показать еще
            </button>
          </div>
        )}
      </main>

      <PostModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreatePost}
        loading={actionLoading}
      />
    </div>
  );
};