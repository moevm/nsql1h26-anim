import { useState } from 'react';
import { Header } from '@components/header';
import { request } from '@api/axios';
import {
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer
} from 'recharts';
import styles from './StatsPage.module.css';

const TABS = [
  { id: 'posts', label: 'Посты' },
  { id: 'users', label: 'Пользователи' },
  { id: 'comments', label: 'Комментарии' },
];

const TAXON_OPTIONS = [
  { value: 'mammal', label: 'Млекопитающее' },
  { value: 'bird', label: 'Птица' },
  { value: 'reptile', label: 'Рептилия' },
  { value: 'amphibian', label: 'Земноводное' },
  { value: 'fish', label: 'Рыба' },
  { value: 'invertebrate', label: 'Беспозвоночное' },
];

const X_OPTIONS = {
  posts: [
    { value: 'type', label: 'Тип поста' },
    { value: 'tag', label: 'Тег' },
    { value: 'taxon', label: 'Таксон' },
    { value: 'author', label: 'Автор' },
    { value: 'date', label: 'Дата' },
  ],
  users: [
    { value: 'role', label: 'Роль' },
    { value: 'username', label: 'Имя пользователя' },
    { value: 'first_name', label: 'Имя' },
    { value: 'last_name', label: 'Фамилия' },
  ],
  comments: [
    { value: 'author', label: 'Автор' },
  ],
};

const Y_OPTIONS = {
  posts: [
    { value: 'count', label: 'Количество постов' },
    { value: 'likes_count', label: 'Лайки' },
    { value: 'comments_count', label: 'Комментарии' },
  ],
  users: [
    { value: 'count', label: 'Количество пользователей' },
    { value: 'followers_count', label: 'Подписчики' },
    { value: 'following_count', label: 'Подписки' },
    { value: 'posts_count', label: 'Посты' },
    { value: 'likes_count', label: 'Лайки' },
    { value: 'comments_count', label: 'Комментарии' },
  ],
  comments: [
    { value: 'count', label: 'Количество комментариев' },
    { value: 'likes_count', label: 'Лайки' },
  ],
};

const COLORS = [
  '#386a51', '#2563eb', '#e11d48', '#7c3aed',
  '#d97706', '#0891b2', '#65a30d', '#db2777',
];

const emptyFilters = {
  posts: { author: '', tag: '', taxon: '', type: '' },
  users: { first_name: '', last_name: '', username: '', role: '' },
  comments: { author: '' },
};

export const StatsPage = () => {
  const [tab, setTab] = useState('posts');
  const [xField, setXField] = useState('type');
  const [yField, setYField] = useState('count');
  const [filters, setFilters] = useState(emptyFilters);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTabChange = (id) => {
    setTab(id);
    setXField(X_OPTIONS[id][0].value);
    setYField(Y_OPTIONS[id][0].value);
    setChartData(null);
    setError('');
  };

  const setFilter = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [tab]: { ...prev[tab], [key]: value },
    }));
  };

  const resetFilters = () => {
    setFilters(prev => ({ ...prev, [tab]: { ...emptyFilters[tab] } }));
  };

  const handleBuild = async () => {
    setLoading(true);
    setError('');
    setChartData(null);
    try {
      const cleanFilters = Object.fromEntries(
        Object.entries(filters[tab]).filter(([_, v]) => v !== '')
      );
      const data = await request('get', `stats/${tab}`, {
        x_field: xField,
        y_field: yField,
        ...cleanFilters,
      });

      const transformed = buildChartData(data.rows, yField);
      setChartData({ data: transformed, rows: data.rows });
    } catch (err) {
      setError(err?.response?.data?.error?.message || 'Ошибка при загрузке данных');
    } finally {
      setLoading(false);
    }
  };

  const buildChartData = (rows, yField) => {
    const xValues = [...new Set(rows.map(r => String(r.x ?? '—')))];
    const yValues = [...new Set(rows.map(r => String(r.y ?? '—')))];

    return xValues.map(xVal => {
      const entry = { x: xVal };
      yValues.forEach(yVal => {
        const row = rows.find(
          r => String(r.x ?? '—') === xVal && String(r.y ?? '—') === yVal
        );
        entry[yVal] = row ? row.count : 0;
      });
      return entry;
    });
  };

  const yKeys = chartData
    ? [...new Set(chartData.rows.map(r => String(r.y ?? '—')))]
    : [];

  const f = filters[tab];

  return (
    <div className={styles.wrapper}>
      <Header />
      <main className={styles.main}>
        <div className={styles.pageHeader}>
          <h1>Статистика</h1>
          <p>Анализируйте данные сообщества по постам, пользователям и комментариям</p>
        </div>

        <div className={styles.tabs}>
          {TABS.map(t => (
            <button
              key={t.id}
              className={tab === t.id ? styles.tabActive : styles.tab}
              onClick={() => handleTabChange(t.id)}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div className={styles.card}>
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Фильтры</h2>

            {tab === 'posts' && (
              <div className={styles.filtersGrid}>
                <div className={styles.filterGroup}>
                  <label>Автор</label>
                  <input
                    placeholder="username"
                    value={f.author}
                    onChange={e => setFilter('author', e.target.value)}
                  />
                </div>
                <div className={styles.filterGroup}>
                  <label>Тег</label>
                  <input
                    placeholder="Например: лес"
                    value={f.tag}
                    onChange={e => setFilter('tag', e.target.value)}
                  />
                </div>
                <div className={styles.filterGroup}>
                  <label>Таксон</label>
                  <select value={f.taxon} onChange={e => setFilter('taxon', e.target.value)}>
                    <option value="">Все</option>
                    {TAXON_OPTIONS.map(o => (
                      <option key={o.value} value={o.value}>{o.label}</option>
                    ))}
                  </select>
                </div>
                <div className={styles.filterGroup}>
                  <label>Тип поста</label>
                  <select value={f.type} onChange={e => setFilter('type', e.target.value)}>
                    <option value="">Все</option>
                    <option value="note">Заметка</option>
                    <option value="animal">Животное</option>
                  </select>
                </div>
              </div>
            )}

            {tab === 'users' && (
              <div className={styles.filtersGrid}>
                <div className={styles.filterGroup}>
                  <label>Имя</label>
                  <input
                    placeholder="Имя"
                    value={f.first_name}
                    onChange={e => setFilter('first_name', e.target.value)}
                  />
                </div>
                <div className={styles.filterGroup}>
                  <label>Фамилия</label>
                  <input
                    placeholder="Фамилия"
                    value={f.last_name}
                    onChange={e => setFilter('last_name', e.target.value)}
                  />
                </div>
                <div className={styles.filterGroup}>
                  <label>Username</label>
                  <input
                    placeholder="username"
                    value={f.username}
                    onChange={e => setFilter('username', e.target.value)}
                  />
                </div>
                <div className={styles.filterGroup}>
                  <label>Роль</label>
                  <select value={f.role} onChange={e => setFilter('role', e.target.value)}>
                    <option value="">Все</option>
                    <option value="user">Пользователь</option>
                    <option value="admin">Администратор</option>
                  </select>
                </div>
              </div>
            )}

            {tab === 'comments' && (
              <div className={styles.filtersGrid}>
                <div className={styles.filterGroup}>
                  <label>Автор</label>
                  <input
                    placeholder="username"
                    value={f.author}
                    onChange={e => setFilter('author', e.target.value)}
                  />
                </div>
              </div>
            )}
          </div>

          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Оси</h2>
            <div className={styles.filtersGrid}>
              <div className={styles.filterGroup}>
                <label>Ось X</label>
                <select value={xField} onChange={e => setXField(e.target.value)}>
                  {X_OPTIONS[tab].map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
              <div className={styles.filterGroup}>
                <label>Ось Y</label>
                <select value={yField} onChange={e => setYField(e.target.value)}>
                  {Y_OPTIONS[tab].map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {error && <div className={styles.error}>{error}</div>}

          <div className={styles.actions}>
            <button className={styles.buildBtn} onClick={handleBuild} disabled={loading}>
              {loading ? 'Загрузка...' : 'Построить диаграмму'}
            </button>
            <button className={styles.resetBtn} onClick={resetFilters}>
              Сбросить фильтры
            </button>
          </div>
        </div>

        {chartData && chartData.data.length > 0 && (
          <div className={styles.chartCard}>
            <h2 className={styles.chartTitle}>
              {TABS.find(t => t.id === tab)?.label} — X: {X_OPTIONS[tab].find(o => o.value === xField)?.label}, Y: {Y_OPTIONS[tab].find(o => o.value === yField)?.label}
            </h2>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={chartData.data} margin={{ top: 10, right: 30, left: 0, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="x" angle={-35} textAnchor="end" interval={0} tick={{ fontSize: 12 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Legend verticalAlign="top" />
                {yKeys.map((key, i) => (
                  <Bar key={key} dataKey={key} fill={COLORS[i % COLORS.length]} radius={[4, 4, 0, 0]} />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {chartData && chartData.data.length === 0 && (
          <div className={styles.empty}>Нет данных для выбранных параметров</div>
        )}
      </main>
    </div>
  );
};