import { Header } from "@components/header";
import { 
  HiOutlineLocationMarker, 
  HiOutlineHeart, 
  HiOutlineChatAlt, 
  HiOutlineTrash 
} from "react-icons/hi";
import styles from './FeedPage.module.css';

export const FeedPage = () => {
  const posts = [
    {
      id: 1,
      authorInitials: 'AL',
      authorName: 'alexnature',
      date: '25 ноября 2025 г.',
      title: 'Медведь ловит рыбу',
      image: 'https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&q=80&w=800',
      description: 'Бурый медведь на перекате реки ловил лосося. За час поймал не меньше пяти рыб. Техника поражает: он просто стоит и ждет, пока рыба сама прыгнет в лапы.',
      hashtags: ['#медведь', '#рыбалка', '#река', '#лосось'],
      location: 'река Тунгуска, Сахалин',
      likes: 2,
      comments: 0,
    },
    {
      id: 2,
      authorInitials: 'WI',
      authorName: 'wildwatcher',
      date: '20 ноября 2025 г.',
      title: 'Серая неясыть на дубе',
      description: 'Эта сова сидела на одном месте всё утро. Полностью игнорировала меня, пока я снимал её с дистанции 15 метров. Удивительная маскировка под кору дерева.',
      hashtags: ['#сова', '#неясыть', '#птица', '#парк'],
      location: 'Павловский парк, Санкт-Петербург',
      likes: 5,
      comments: 2,
    },
    {
      id: 3,
      authorInitials: 'BI',
      authorName: 'birdlover99',
      date: '15 ноября 2025 г.',
      title: 'Волки в зимнем лесу',
      image: 'https://images.unsplash.com/photo-1590420485404-f86d22b8abf8?auto=format&fit=crop&q=80&w=800',
      description: 'Следил за волчьей стаей три часа. Они шли по своему обычному маршруту через ельник. Вожак постоянно оглядывался, проверяя тылы стаи.',
      hashtags: ['#волк', '#стая', '#зима', '#заповедник'],
      location: 'Витимский заповедник, Урал',
      likes: 8,
      comments: 3,
    },
    {
      id: 4,
      authorInitials: 'FO',
      authorName: 'fox_hunter',
      date: '10 ноября 2025 г.',
      title: 'Рыжая лиса в поле',
      image: 'https://images.unsplash.com/photo-1474511320723-9a56873867b5?auto=format&fit=crop&q=80&w=800',
      description: 'Лиса охотилась на мышей-полевок. Её прыжки в снег выглядят невероятно грациозно и точно. Удалось поймать момент в прыжке.',
      hashtags: ['#лиса', '#охота', '#природа', '#поле'],
      location: 'Кроноцкий заповедник, Камчатка',
      likes: 12,
      comments: 4,
    },
    {
      id: 5,
      authorInitials: 'DE',
      authorName: 'deer_scout',
      date: '05 ноября 2025 г.',
      title: 'Благородный олень',
      image: 'https://images.unsplash.com/photo-1484406566174-9da000fda645?auto=format&fit=crop&q=80&w=800',
      description: 'Ранним утром в тумане появился этот красавец. Рога просто огромные. Он учуял меня через пару минут и скрылся в чаще леса.',
      hashtags: ['#олень', '#лес', '#туман', '#утро'],
      location: 'Национальный парк "Лосиный остров"',
      likes: 20,
      comments: 7,
    },
    {
      id: 6,
      authorInitials: 'EA',
      authorName: 'eagle_eye',
      date: '01 ноября 2025 г.',
      title: 'Белоголовый орлан',
      image: 'https://images.unsplash.com/photo-1454537468202-b7ff71d51c2e?auto=format&fit=crop&q=80&w=800',
      description: 'Хищник высматривал добычу с вершины старой сосны. Размах крыльев этой птицы достигает двух метров. Величественное зрелище.',
      hashtags: ['#орел', '#орлан', '#небо', '#хищник'],
      location: 'Байкальский заповедник',
      likes: 15,
      comments: 1,
    }
  ];

  return (
    <div className={styles.feedWrapper}>
      <Header />
      <main className={styles.mainContent}>
        <div className={styles.lentaHeader}>
          <h2 className={styles.lentaTitle}>Лента наблюдений</h2>
          <p className={styles.lentaSubtitle}>Делитесь своими открытиями дикой природы</p>
        </div>

        <div className={styles.counterWrapper}>
          <p className={styles.counterText}>
            Показано <span className={styles.counterNumber}>{posts.length}</span> из{' '}
            <span className={styles.counterNumber}>{posts.length} наблюдений</span>
          </p>
        </div>

        <div className={styles.postsList}>
          {posts.map((post) => (
            <article key={post.id} className={styles.postCard}>
              {post.image && (<img src={post.image} alt={post.title} className={styles.postImageStub} />)}
              
              <div className={styles.cardBody}>
                <div className={styles.authorSection}>
                  <div className={styles.authorAvatar}>
                    <span className={styles.authorInitials}>{post.authorInitials}</span>
                  </div>
                  <div className={styles.authorInfo}>
                    <span className={styles.authorName}>{post.authorName}</span>
                    <span className={styles.postDate}>{post.date}</span>
                  </div>
                </div>

                <div className={styles.postContent}>
                  <h3 className={styles.postTitle}>{post.title}</h3>
                  <p className={styles.postDescription}>{post.description}</p>

                  <div className={styles.hashtags}>
                    {post.hashtags.map((tag, idx) => (
                      <span key={idx} className={styles.hashtag}>
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className={styles.location}>
                    <HiOutlineLocationMarker className={styles.locationIcon} />
                    <span className={styles.locationText}>{post.location}</span>
                  </div>

                  <div className={styles.postStats}>
                    <div className={styles.statGroup}>
                      <span className={styles.statItem}>
                        <HiOutlineHeart /> {post.likes}
                      </span>
                      <span className={styles.statItem}>
                        <HiOutlineChatAlt /> {post.comments}
                      </span>
                    </div>
                    <HiOutlineTrash className={styles.deleteBtn} />
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      </main>
    </div>
  );
};