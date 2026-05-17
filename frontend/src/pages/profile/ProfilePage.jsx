import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '@contexts/index';
import { request } from '@api/axios';
import { Header } from '@components/header';
import { ProfileHeader, ProfileStats } from '@components/profile';
import { PostCard } from '@components/post/post-card/PostCard';
import { UserCard } from '@components/user-card';
import styles from './ProfilePage.module.css';

export const ProfilePage = () => {
  const { userId } = useParams();
  const { user: currentUser } = useAuth();
  const navigate = useNavigate();

  const profileId = userId || currentUser?.id;
  const isOwn = !userId || userId === currentUser?.id;

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('posts');
  const [editing, setEditing] = useState(false);
  const [followLoading, setFollowLoading] = useState(false);
  const [tabData, setTabData] = useState({ items: [], loading: false });

  const [editForm, setEditForm] = useState({ bio: '', avatarUrl: '', avatarBackgroundColor: '' });

  const fetchUser = useCallback(async () => {
    if (!profileId) return;
    try {
      const data = await request('get', `users/${profileId}`);
      setUser(data);
      setEditForm({
        bio: data.bio || '',
        avatarUrl: data.avatarUrl || '',
        avatarBackgroundColor: data.avatarBackgroundColor || '#4a7c66',
      });
    } catch (err) {
      console.error("User not found", err);
      navigate('/');
    } finally {
      setLoading(false);
    }
  }, [profileId, navigate]);

  const fetchTabData = useCallback(async () => {
    if (!profileId) return;
    setTabData(prev => ({ ...prev, loading: true }));

    try {
      let res;
      if (activeTab === 'posts') {
        res = await request('get', 'posts', { 
          author: profileId,
          limit: 20
        });
      } else {
        res = await request('get', `users/${profileId}/${activeTab}`);
      }
      const items = res?.items || (Array.isArray(res) ? res : []);
      setTabData({ items, loading: false });
    } catch (err) {
      console.error("Ошибка загрузки вкладок:", err);
      setTabData({ items: [], loading: false });
    }
  }, [activeTab, profileId]);

  useEffect(() => { fetchUser(); }, [fetchUser]);
  useEffect(() => { fetchTabData(); }, [fetchTabData]);

  const handleSave = async () => {
    try {
      await request('patch', 'users/me', editForm);
      await fetchUser();
      setEditing(false);
    } catch (err) {
      alert('Ошибка сохранения');
    }
  };

  const handleFollow = async () => {
    if (followLoading) return;
    setFollowLoading(true);
    try {
      await request('post', `users/${profileId}/follow`);
      await fetchUser();
    } catch (err) {
      console.error("Follow error", err);
    } finally {
      setFollowLoading(false);
    }
  };

  const handleFollowUser = async (targetId) => {
    try {
      await request('post', `users/${targetId}/follow`);
      setTabData(prev => ({
        ...prev,
        items: prev.items.map(item => 
          item.id === targetId ? { ...item, isFollowed: !item.isFollowed } : item
        )
      }));
      if (isOwn) fetchUser();
    } catch (err) {
      console.error("Error toggling follow", err);
    }
  };

  if (loading) return <div className={styles.loader}>Загрузка...</div>;
  if (!user) return null;

  const tabs = [
    { id: 'posts', label: 'Наблюдения', count: user.postsCount },
    { id: 'followers', label: 'Подписчики', count: user.followersCount },
    { id: 'following', label: 'Подписки', count: user.followingCount }
  ];

  return (
    <div className={styles.layout}>
      <Header />
      <main className={styles.container}>
        <section className={styles.topSection}>
          <ProfileHeader 
            isOwn={isOwn}
            editing={editing}
            user={user}
            editForm={editForm}
            setEditForm={setEditForm}
            onEdit={() => setEditing(true)}
            onCancel={() => setEditing(false)}
            onSave={handleSave}
            onFollow={handleFollow}
            followLoading={followLoading}
          />
          <ProfileStats user={user} />
        </section>

        <section className={styles.contentSection}>
          <div className={styles.tabs}>
            {tabs.map(t => (
              <button 
                key={t.id}
                className={activeTab === t.id ? styles.tabActive : styles.tab}
                onClick={() => setActiveTab(t.id)}
              >
                {t.label} <span>{t.count || 0}</span>
              </button>
            ))}
          </div>

          <div className={styles.grid}>
            {tabData.loading ? (
              <div className={styles.tabLoader}>Загрузка...</div>
            ) : tabData.items.length === 0 ? (
              <div className={styles.empty}>Здесь пока пусто</div>
            ) : activeTab === 'posts' ? (
              <div className={styles.postsGrid}>
                {tabData.items.map(post => <PostCard key={post.id} post={post} />)}
              </div>
            ) : (
              <div className={styles.usersList}>
                {tabData.items.map(u => (
                  <UserCard 
                    key={u.id} 
                    user={u} 
                    isOwn={u.id === currentUser?.id}
                    onFollow={() => handleFollowUser(u.id)}
                  />
                ))}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
};