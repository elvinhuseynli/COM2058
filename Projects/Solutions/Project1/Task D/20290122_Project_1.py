import psycopg2
connection = psycopg2.connect(database="20290122", user="postgres", password="elvin2003", host="localhost", port="5432")
cursor = connection.cursor()
 
# Question-1
print(str('Question-1\n'))
q1 = "select order_id, (unit_price*quantity) as total_price, (unit_price*quantity*(1-discount)) as discounted_price from order_details order by discounted_price desc limit 10;"
cursor.execute(q1)

rows = cursor.fetchall()
print("{:<8} {:<20} {:<15}".format('OrderId', 'TotalPrice', 'TotalwithDiscountPrice'))
for row in rows:
    print("{:<8} {:<20} {:<15}".format(row[0], row[1], row[2]))
print("\n")

#----------------------------------------------------------------------------------------------#
# Question-2

print(str('Question-2\n'))
q2 = "create view ret as((select shipped_date, od.order_id, (od.unit_price*od.quantity) as total_price,extract(year from shipped_date) as years from orders inner join order_details od on od.order_id = orders.order_id where shipped_date between '1997-12-30' and '1996-01-05' order by shipped_date asc, order_id asc) union all (select shipped_date, od.order_id, sum(od.unit_price*od.quantity) total_price, extract(year from shipped_date) as years from orders inner join order_details od on od.order_id = orders.order_id group by shipped_date, od.order_id, years order by order_id asc));(select shipped_date, od.order_id, sum(od.unit_price*od.quantity) total_price, extract(year from shipped_date)::numeric as years from orders inner join order_details od on od.order_id = orders.order_id where shipped_date between '1997-12-30' and '1998-01-05' group by shipped_date, od.order_id, years order by shipped_date asc, order_id asc) union all (select ret.shipped_date, ret.order_id, ret.total_price, ret.years::numeric from ret where ret.shipped_date is null and ret.total_price>4000 group by ret.shipped_date, ret.order_id, ret.years, ret.total_price)"
cursor.execute(q2)
rows = cursor.fetchall()
print("{:<15} {:<8} {:<20} {:<8}".format('ShippedDate', 'OrderId', 'TotalPrice', 'Years'))
for row in rows:
	print("{:<15} {:<8} {:<20} {:<8}".format(str(row[0]), row[1], str(row[2]), str(row[3])))
print('\n')

#----------------------------------------------------------------------------------------------#
# Question-3

print(str('Question-3\n'))
q3 = "select categories.category_name, products.category_id, products.product_name, products.product_id,products.unit_price, products.units_in_stock, products.units_on_order, products.reorder_level,products.discontinued from categories right join products on products.category_id = categories.category_id where discontinued=0 and reorder_level>20 and units_on_order=0 order by product_name;"
cursor.execute(q3)
rows = cursor.fetchall()
print("{:<20} {:<15} {:<33} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format('CategoryName','CategoryId','ProductName','ProductId','UnitPrice','UnitsInStock','UnitsOnOrder','ReorderLevel','Discontinued'))
for row in rows:
	print("{:<20} {:<15} {:<33} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
print('\n')


#----------------------------------------------------------------------------------------------#
# Question-4

print(str('Question-4\n'))
q4 = "(select orders.ship_name, orders.ship_country, customers.customer_id, customers.company_name, concat(employees.first_name ,' ' , employees.last_name) as salesperson , shippers.phone, products.product_id, products.product_name, orders.freight from orders right join employees on employees.employee_id = orders.employee_id right join customers on customers.customer_id = orders.customer_id right join shippers on shippers.shipper_id = orders.ship_via left join order_details on orders.order_id = order_details.order_id left join products on products.product_id = order_details.product_id where orders.ship_country like 'I%y' and ship_name like 'M%' and freight>70 order by salesperson asc) union all (select orders.ship_name, orders.ship_country, customers.customer_id, customers.company_name, concat(employees.first_name ,' ' , employees.last_name) as salesperson , shippers.phone, products.product_id, products.product_name, orders.freight from orders right join employees on employees.employee_id = orders.employee_id right join customers on customers.customer_id = orders.customer_id right join shippers on shippers.shipper_id = orders.ship_via left join order_details on orders.order_id = order_details.order_id left join products on products.product_id = order_details.product_id where orders.ship_country like 'G%y' and ship_name like 'M%' and freight>70 order by salesperson asc);"
cursor.execute(q4)
rows = cursor.fetchall()
print("{:<30} {:<13} {:<13} {:<30} {:<20} {:<15} {:<10} {:<30} {:<8}".format('ShipName','ShipCountry','CustomerId','CompanyName','SalesPerson','Phone','ProductId','ProductName','Freight'))
for row in rows:
	print("{:<30} {:<13} {:<13} {:<30} {:<20} {:<15} {:<10} {:<30} {:<8}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
print('\n')


#----------------------------------------------------------------------------------------------#
# Question-5

print(str('Question-5\n'))
q5 = "alter table orders add \"Year 1999\" double precision,add \"Year 1998\" double precision,add \"Year 1997\" double precision,add \"Year 1996\" double precision;update orders set \"Year 1999\" = 0;update orders set \"Year 1998\" = 0;update orders set \"Year 1997\" = 0; update orders set \"Year 1996\" = 0; (select od.product_id, orders.customer_id, extract(year from orders.order_date)::numeric as \"year\", \"Year 1999\",\"Year 1998\",\"Year 1997\", (od.unit_price*od.quantity*(1-od.discount)) as \"Year 1996\" from orders right join order_details od on od.order_id = orders.order_id where od.product_id < 5 and orders.customer_id like 'E%' and extract(year from orders.order_date) = 1996 order by \"year\", od.product_id) union all (select od.product_id, orders.customer_id, extract(year from orders.order_date)::numeric as \"year\", \"Year 1999\",\"Year 1998\",(od.unit_price*od.quantity*(1-od.discount)) as \"Year 1997\", \"Year 1996\"from orders right join order_details od on od.order_id = orders.order_id where od.product_id < 5 and orders.customer_id like 'E%' and extract(year from orders.order_date) = 1997 order by \"year\", od.product_id) union all (select od.product_id, orders.customer_id, extract(year from orders.order_date)::numeric as \"year\",\"Year 1999\",(od.unit_price*od.quantity*(1-od.discount)) as \"Year 1998\",\"Year 1997\",\"Year 1996\" from orders right join order_details od on od.order_id = orders.order_id where od.product_id < 5 and orders.customer_id like 'E%' and extract(year from orders.order_date) = 1998 order by \"year\", od.product_id) union all (select od.product_id, orders.customer_id, extract(year from orders.order_date)::numeric as \"year\", (od.unit_price*od.quantity*(1-od.discount)) as \"Year 1999\",\"Year 1998\",\"Year 1997\",\"Year 1996\" from orders right join order_details od on od.order_id = orders.order_id where od.product_id < 5 and orders.customer_id like 'E%' and extract(year from orders.order_date) = 1999 order by \"year\", od.product_id)"
cursor.execute(q5)
rows = cursor.fetchall()
print("{:<10} {:<15} {:<15} {:<15} {:<15} {:<20} {:<15}".format('ProductId','CustomerId','Year','Year 1999','Year 1998','Year 1997','Year 1996'))
for row in rows:
	print("{:<10} {:<15} {:<15} {:<15} {:<15} {:<20} {:<15}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
print('\n')

#----------------------------------------------------------------------------------------------#
# Question-6

print(str('Question-6\n'))
q6 = "(select 'Customers' as tablename, city, company_name, contact_name from customers where contact_name like '%w%') union (select 'Suppliers' as tablename, city, company_name, contact_name from suppliers where contact_name like '%g%') order by contact_name asc;"
cursor.execute(q6)
rows = cursor.fetchall()
print("{:<15} {:<15} {:<30} {:<25}".format('TableName','City','CompanyName','ContactName'))
for row in rows:
	print("{:<15} {:<15} {:<30} {:<25}".format(row[0],row[1],row[2],row[3]))
print('\n')

#----------------------------------------------------------------------------------------------#
# Question-7

print(str('Question-7\n'))
q7 = "create view btm as((select product_name as Product_Names, unit_price as Prices from products order by Prices desc limit 5) union all (select product_name as Product_Names, unit_price as Prices from products order by  Prices asc limit 5));select Product_names, Prices from btm order by Prices desc;"
cursor.execute(q7)
rows = cursor.fetchall()
print("{:<25} {:<10}".format('ProductName','Prices'))
for row in rows:
	print("{:<25} {:<10}".format(row[0],row[1]))
print('\n')

#----------------------------------------------------------------------------------------------#
# Question-8

print(str('Question-8\n'))
q8="select extract(year from orders.shipped_date)::numeric as shippedyear, categories.category_name, round(sum(order_details.unit_price*quantity*(1-discount))::numeric,2) as category_sales from  order_details right join orders on orders.order_id = order_details.order_id right join products on  order_details.product_id = products.product_id right join categories on categories.category_id = products.category_id where orders.shipped_date>'1997-05-31' group by category_name, shippedyear order by shippedyear;"
cursor.execute(q8)
rows = cursor.fetchall()
print("{:<15} {:<20} {:<10}".format('ShippedYear','CategoryName','CategorySales'))
for row in rows:
	print("{:<15} {:<20} {:<10}".format(row[0],row[1],row[2]))	
print('\n')

connection.commit()
connection.close()