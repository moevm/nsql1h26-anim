import { 
  HiOutlineSearch, 
  HiOutlineX, 
  HiOutlineAdjustments 
} from "react-icons/hi";
import styles from './PostFilters.module.css';

const TAXON_OPTIONS = [
  { value: 'mammal', label: 'Млекопитающее' },
  { value: 'bird', label: 'Птица' },
  { value: 'reptile', label: 'Рептилия' },
  { value: 'amphibian', label: 'Земноводное' },
  { value: 'fish', label: 'Рыба' },
  { value: 'invertebrate', label: 'Беспозвоночное' },
];

export const PostFilters = ({ 
  filters, 
  setFilter, 
  resetFilters, 
  filtersOpen, 
  setFiltersOpen 
}) => {
  const activeFiltersCount = [
    filters.taxon, filters.tag, filters.author,
    filters.dateFrom, filters.dateTo, filters.onlyFollowed,
  ].filter(Boolean).length;

  return (
    <div className={styles.filtersPanel}>
      <div className={styles.searchRow}>
        <div className={styles.searchWrap}>
          <HiOutlineSearch className={styles.searchIcon} />
          <input
            className={styles.searchInput}
            placeholder="Поиск по постам..."
            defaultValue={filters.search}
            onChange={(e) => setFilter('search', e.target.value)}
          />
          {filters.search && (
            <HiOutlineX 
              className={styles.searchClear} 
              onClick={() => setFilter('search', '')} 
            />
          )}
        </div>
        <button
          className={`${styles.filtersToggle} ${filtersOpen ? styles.filtersToggleActive : ''}`}
          onClick={() => setFiltersOpen(p => !p)}
        >
          <HiOutlineAdjustments />
          Фильтры
          {activeFiltersCount > 0 && (
            <span className={styles.filtersBadge}>{activeFiltersCount}</span>
          )}
          <span className={styles.arrow}>{filtersOpen ? '∧' : '∨'}</span>
        </button>
      </div>

      {filtersOpen && (
        <div className={styles.filtersBody}>
          <label className={styles.followedCheck}>
            <input
              type="checkbox"
              checked={filters.onlyFollowed}
              onChange={(e) => setFilter('onlyFollowed', e.target.checked)}
            />
            <span>Только от подписок</span>
          </label>

          <div className={styles.filterRow}>
            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>СОРТИРОВКА</label>
              <select
                className={styles.filterSelect}
                value={filters.sort}
                onChange={(e) => setFilter('sort', e.target.value)}
              >
                <option value="newest">Сначала новые</option>
                <option value="oldest">Сначала старые</option>
                <option value="popular">По популярности</option>
              </select>
            </div>

            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>АВТОР</label>
              <input
                className={styles.filterInput}
                placeholder="Имя пользователя"
                value={filters.author}
                onChange={(e) => setFilter('author', e.target.value)}
              />
            </div>

            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>ТАКСОН</label>
              <select
                className={styles.filterSelect}
                value={filters.taxon}
                onChange={(e) => setFilter('taxon', e.target.value)}
              >
                <option value="">Все</option>
                {TAXON_OPTIONS.map(o => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </div>

            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>НАУЧНОЕ НАЗВАНИЕ</label>
              <input
                className={styles.filterInput}
                placeholder="Например: Vulpes"
                value={filters.scientificName || ''}
                onChange={(e) => setFilter('scientificName', e.target.value)}
              />
            </div>
            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>ТЕГ</label>
              <input
                className={styles.filterInput}
                placeholder="Например: лес"
                value={filters.tag}
                onChange={(e) => setFilter('tag', e.target.value)}
              />
            </div>
          </div>
          <div className={styles.filterRow}>
            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>ДАТА С</label>
              <input
                type="date"
                className={styles.filterInput}
                value={filters.dateFrom}
                onChange={(e) => setFilter('dateFrom', e.target.value)}
              />
            </div>
            <div className={styles.filterGroup}>
              <label className={styles.filterLabel}>ДАТА ПО</label>
              <input
                type="date"
                className={styles.filterInput}
                value={filters.dateTo}
                onChange={(e) => setFilter('dateTo', e.target.value)}
              />
            </div>
            <div className={styles.resetWrapper}>
              {activeFiltersCount > 0 && (
                <button className={styles.resetBtn} onClick={resetFilters}>
                  <HiOutlineX /> Сбросить все
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};