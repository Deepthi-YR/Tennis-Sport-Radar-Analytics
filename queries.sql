-- COMPETITIONS
-- 1. All competitions with their category
SELECT cp.competition_name, ca.category_name FROM competitions cp JOIN categories ca ON cp.category_id=ca.category_id ORDER BY ca.category_name, cp.competition_name;
-- 2. Competition count by category
SELECT ca.category_name, COUNT(*) competition_count FROM categories ca LEFT JOIN competitions cp ON ca.category_id=cp.category_id GROUP BY ca.category_name ORDER BY competition_count DESC;
-- 3. Doubles competitions
SELECT * FROM competitions WHERE LOWER(type)='doubles';
-- 4. Competitions in a selected category (parameter: :category_name)
SELECT cp.* FROM competitions cp JOIN categories ca ON cp.category_id=ca.category_id WHERE ca.category_name=:category_name;
-- 5. Parent and child competitions
SELECT parent.competition_name parent_competition, child.competition_name sub_competition FROM competitions child JOIN competitions parent ON child.parent_id=parent.competition_id ORDER BY parent_competition;
-- 6. Type distribution by category
SELECT ca.category_name, cp.type, COUNT(*) total FROM competitions cp JOIN categories ca ON cp.category_id=ca.category_id GROUP BY ca.category_name, cp.type ORDER BY ca.category_name, total DESC;
-- 7. Top-level competitions
SELECT * FROM competitions WHERE parent_id IS NULL;

-- COMPLEXES AND VENUES
-- 8. Venues with complex
SELECT v.venue_name, c.complex_name FROM venues v JOIN complexes c ON v.complex_id=c.complex_id;
-- 9. Venue count by complex
SELECT c.complex_name, COUNT(v.venue_id) venue_count FROM complexes c LEFT JOIN venues v ON c.complex_id=v.complex_id GROUP BY c.complex_name;
-- 10. Venues in a country (parameter: :country_name)
SELECT * FROM venues WHERE country_name=:country_name;
-- 11. Venues and timezones
SELECT venue_name, timezone FROM venues ORDER BY venue_name;
-- 12. Complexes with more than one venue
SELECT c.complex_name, COUNT(*) venue_count FROM complexes c JOIN venues v ON c.complex_id=v.complex_id GROUP BY c.complex_name HAVING COUNT(*)>1;
-- 13. Venues grouped by country
SELECT country_name, GROUP_CONCAT(venue_name, ', ') venues FROM venues GROUP BY country_name;
-- 14. Venues for a selected complex (parameter: :complex_name)
SELECT v.* FROM venues v JOIN complexes c ON v.complex_id=c.complex_id WHERE c.complex_name=:complex_name;

-- DOUBLES RANKINGS
-- 15. Competitors with rank and points
SELECT c.name, r.rank, r.points FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id ORDER BY r.rank;
-- 16. Top five competitors
SELECT c.name, r.rank, r.points FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id ORDER BY r.rank LIMIT 5;
-- 17. Stable ranks
SELECT c.name, r.rank FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id WHERE r.movement=0;
-- 18. Total points from a country (parameter: :country_name)
SELECT c.country, SUM(r.points) total_points FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id WHERE c.country=:country_name GROUP BY c.country;
-- 19. Competitor count per country
SELECT country, COUNT(*) competitors FROM competitors GROUP BY country ORDER BY competitors DESC;
-- 20. Current-week highest points
SELECT c.name, r.points FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id WHERE r.points=(SELECT MAX(points) FROM competitor_rankings);
