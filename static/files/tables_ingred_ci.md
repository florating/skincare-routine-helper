## Generated on 11/05/2021

project_test_2=# SELECT c.category_id, c.category_name, COUNT(p.product_name) AS num_products FROM categories AS c FULL OUTER JOIN products AS p ON (c.category_id= p.category_id) GROUP BY c.category_id ORDER BY c.category_id;
| category_id | category_name | num_products  |
|-------------|---------------|-------------- |
|           1 | Cleanser      |           95 |
|           2 | Exfoliator    |           43 |
|           3 | Peel          |           31 |
|           4 | Toner         |           63 |
|           5 | Essence       |            0 |
|           6 | Serum         |           92 |
|           7 | Mist          |           71 |
|           8 | Mask          |          113 |
|           9 | Moisturizer   |          100 |
|          10 | Eye Care      |           93 |
|          11 | Oil           |           22 |
|          12 | Sunscreen     |            0 |
|          13 | Balm          |           20 |
|          14 | Bath Salts    |            0 |
|          15 | Body Wash     |            0 |
|          16 | Bath Oil      |            0 |
(16 rows)


```psql
project_test_2=# SELECT ingredient_id, common_name FROM ingredients WHERE common_name ILIKE 'CI %';
```
| ingredient_id |        common_name         |
|---------------|----------------------------|
|            37 | ci 77019 |
|            38 | ci 77491      |
|           147 | ci 77492      |
|           257 | ci 14700      |
|           258 | ci 19140      |
|           265 | ci 42090      |
|           277 | ci 15985      |
|           278 | ci 17200      |
|           293 | ci 16035      |
|           348 | ci 77499      |
|           386 | ci 77289      |
|           794 | ci 77163      |
|           795 | ci 77861      |
|           796 | ci 75470      |
|           827 | ci 17200 (d&c red no33)       |
|           852 | ci 73360      |
|          1232 | ci 60725      |
|          1233 | ci 60725      |
|          1300 | ci 77002      |
|          1380 | ci 61570      |
|          1397 | ci 77480      |
|          1427 | ci 77510      |
|          1470 | ci 77007      |
|          1487 | ci 77489      |
|          1497 | ci 75130      |
|          1540 | ci 77947      |
|          1591 | ci 74160      |
|          1593 | ci 42051      |
|          1681 | ci 61565 / green 6        |
|          1902 | ci 15510      |
|          1924 | ci 15850      |
|          2017 | ci 77000 (aluminum powder)        |
(32 rows)