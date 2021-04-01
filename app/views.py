from flask import render_template, flash, request, redirect, url_for, session, g
from app import app
from .forms import register, changepassword
from .forms import SignIn, filterProducts
from .forms import PickSize, PickSize2, PickSize3, PickSize4, PickSize5, PickSize6, PickSize7
from .forms import PickSize8, PickSize9, PickSize10, PickSize11, PickSize12, PickSize13, PickSize14
from .forms import PickSize15, PickSize16, PickSize17, PickSize18, PickSize19, PickSize20
from app import models,db
import datetime
import random

# Read all of the customers from the database into an array
# This is in a function so that views can call the function (more customers will have registered
# so it needs to be read back into the variable from the database)
def updateallcustomers():
	allCustomers = models.Customers.query.all()
	return allCustomers

@app.before_request
def before_request():
	g.customer = None
	allCustomers = updateallcustomers()
	if 'customerid' in session:
		customer = [x for x in allCustomers if x.customerid == session['customerid']][0]
		g.customer = customer

@app.route('/', methods=['GET', 'POST'])
def home():
	allproducts = models.Products.query.all()
	featuredproducts = [random.choice(allproducts), random.choice(allproducts), random.choice(allproducts)]
	# This code makes sure none of the randomly generated featured products are not the SAME
	while (featuredproducts[0] == featuredproducts[1] or featuredproducts[0] == featuredproducts[2]
			or featuredproducts[1] == featuredproducts[2]):
		if featuredproducts[0] == featuredproducts[1]:
			featuredproducts[0] = random.choice(allproducts)
		if featuredproducts[0] == featuredproducts[2]:
			featuredproducts[0] = random.choice(allproducts)
		if featuredproducts[1] == featuredproducts[2]:
			featuredproducts[1] = random.choice(allproducts)
	newproudcts = [allproducts[len(allproducts)-1], allproducts[len(allproducts)-2], allproducts[len(allproducts)-3]]
	bestsellers = models.Products.query.order_by(models.Products.soldhistory.desc()).all()
	return render_template('home.html', title='Home',home=home, allproducts=allproducts,
							featuredproducts=featuredproducts, newproudcts=newproudcts,
							bestsellers=bestsellers)

@app.route('/account', methods=['GET', 'POST'])
def account():
	form = SignIn()
	if request.method == 'POST':
		session.pop('customerid', None)
		session.pop('basketcontent', None)
		session.pop('sizes', None)
		session.pop('colmode', None)
		email = form.email.data
		password = form.password.data
		allCustomers = updateallcustomers()
		customer = None
		for i in allCustomers:
			if i.email == email:
				customer = i
		if customer and customer.password == password:
			session['customerid'] = customer.customerid
			session['basketcontent'] = []
			session['sizes'] = []
			session['colmode'] = 'light'
			return redirect(url_for('accountinformation'))
		if customer and customer.password != password:
			flash("ERROR: Email recognised but password incorrect")
		else:
			flash('ERROR: Email or password not recognised')
			return redirect(url_for('account'))
	if g.customer:
		return redirect(url_for('accountinformation'))
	return render_template('account.html',title='account', form=form)

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
	if g.customer:
		return redirect(url_for('accountinformation'))
	form = register()
	allCustomers = updateallcustomers()
	if request.method == 'POST':
		if '@' in form.email.data and '.' in form.email.data:
			p = models.Customers(firstname=(form.firstname.data), surname=(form.surname.data),
			email=(form.email.data), password=(form.password.data))
			emailCheck = models.Customers.query.filter_by(email=form.email.data).all()
			if len(emailCheck) == 0:
				if len(form.password.data) < 5:
					flash("ERROR: You're password must be more than 6 characters")
				else:
					db.session.add(p)
					db.session.commit() #commits to the database
					flash('You were successfully registered, now please login below')
					return redirect(url_for('account'))
			else:
				flash('ERROR: You are already registered, please login instead below')
				return redirect(url_for('account')) #redirects to home to show that it is in the list of completed
		else:
			flash("ERROR: Not a valid email address")
	return render_template('register.html', title='signup', form = form)

@app.route('/account-information', methods=['GET', 'POST'])
def accountinformation():
	if not g.customer:
		return redirect(url_for('account'))
	anonpass = "*" * len(g.customer.password)
	return render_template('account-information.html',title='account-information',
	anonpass=anonpass, purchases = g.customer.purchases, numpurchases = len(g.customer.purchases))

@app.route('/password-change', methods=['GET', 'POST'])
def passwordchangepage():
	form = changepassword()
	if not g.customer:
		return redirect(url_for('account'))
	if request.method == 'POST':
		if g.customer.password == form.currentpassword.data:
			if form.newpassword.data == form.confirmpassword.data:
				if len(form.newpassword.data) > 5:
					flash("Password successfully changed. Please log back in")
					currentcustomer = models.Customers.query.get(g.customer.customerid)
					currentcustomer.password = form.newpassword.data
					db.session.commit() #adds to the database
					return redirect(url_for('signout'))
				else:
					flash("ERROR: Password must be 6 characters or longer")
			else:
				flash("ERROR: Your new passwords do not match!")
		else:
			flash("ERROR: Current password incorrect! Please enter your current password you used to log in")
	return render_template('change-password.html',title='change-password',form=form)

# The purpose of this is to sign out the session and then link back to the log in pages
# A sign out button is created and is linked to this page (this page never appears)
@app.route('/sign-out', methods=['GET', 'POST'])
def signout():
	if not g.customer:
		return redirect(url_for('account'))
	else:
		session.pop('customerid', None)
		session.pop('sizes', None)
		session.pop('colmode', None)
		# Need to loop through the basket content and add it all back into the database
		# Without this if you sign out with things in the basket they will all disappear
		# The code below loops through the basket and writes everything back to the database
		for i in range (0, len(session['basketcontent'])):
			p = models.Products.query.get(session['basketcontent'][i])
			if session['sizes'][i] == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel + 1
				db.session.commit() #adds to the database
			if session['sizes'][i] == 'Small (S)':
				p.sstocklevel = p.sstocklevel + 1
				db.session.commit() #adds to the database
			if session['sizes'][i] == 'Medium (M)':
				p.mstocklevel = p.mstocklevel + 1
				db.session.commit() #adds to the database
			if session['sizes'][i] == 'Large (L)':
				p.lstocklevel = p.lstocklevel + 1
				db.session.commit() #adds to the database
			if session['sizes'][i] == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel + 1
				db.session.commit() #adds to the database
		session.pop('basketcontent', None)
		return redirect(url_for('account'))
	return render_template('account-information.html',title='account-information')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
		if session['colmode'] == "light":
			session['colmode'] = "dark"
			session.modified = True
			return redirect(url_for('settings'))
		else:
			session['colmode'] = "light"
			session.modified = True
			return redirect(url_for('settings'))
	return render_template('settings.html', title='about')

#------------------------- PROUDCT PAGES -----------------------------------------------------------

@app.route('/products', methods=['GET', 'POST'])
def products():
	form = filterProducts()
	products = models.Products.query.all() #gets all rows that have completed = 1 (tasks marked completed)
	if request.method == 'POST':
		if form.filter.data == 'Releavance':
			products = models.Products.query.all()
		if form.filter.data == "Price - Low to High":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price > products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
		if form.filter.data == "Price - High to Low":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price < products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
	return render_template('products.html', title='products', products = products, form=form)

@app.route('/products-t-shirts', methods=['GET', 'POST'])
def productstshirts():
	form = filterProducts()
	products = models.Products.query.filter_by(category='T-shirt').all() #gets all rows that have completed = 1 (tasks marked completed)
	if request.method == 'POST':
		if form.filter.data == 'Releavance':
			products = models.Products.query.filter_by(category='T-shirt').all()
		if form.filter.data == "Price - Low to High":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price > products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
		if form.filter.data == "Price - High to Low":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price < products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
	return render_template('products.html', title='products-t-shirts', products = products, form=form)

@app.route('/products-hoodies', methods=['GET', 'POST'])
def productshoodies():
	form = filterProducts()
	products = models.Products.query.filter_by(category='Hoodie').all() #gets all rows that have completed = 1 (tasks marked completed)
	if request.method == 'POST':
		if form.filter.data == 'Releavance':
			products = models.Products.query.filter_by(category='Hoodie').all()
		if form.filter.data == "Price - Low to High":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price > products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
		if form.filter.data == "Price - High to Low":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price < products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
	return render_template('products.html', title='products-hoodies', products = products, form=form)

@app.route('/products-sweats', methods=['GET', 'POST'])
def productssweats():
	form = filterProducts()
	products = models.Products.query.filter_by(category='Sweat').all() #gets all rows that have completed = 1 (tasks marked completed
	if request.method == 'POST':
		if form.filter.data == 'Releavance':
			products = models.Products.query.filter_by(category='Sweat').all()
		if form.filter.data == "Price - Low to High":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price > products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
		if form.filter.data == "Price - High to Low":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price < products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
	return render_template('products.html', title='products-sweats', products = products, form=form)

@app.route('/products-beanies', methods=['GET', 'POST'])
def productsbeanies():
	form = filterProducts()
	products = models.Products.query.filter_by(category='Beanie').all() #gets all rows that have completed = 1 (tasks marked completed)
	if request.method == 'POST':
		if form.filter.data == 'Releavance':
			products = models.Products.query.filter_by(category='Beanie').all()
		if form.filter.data == "Price - Low to High":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price > products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
		if form.filter.data == "Price - High to Low":
			for i in range(0, len(products)):
			    for j in range(i+1, len(products)):
			        if(products[i].price < products[j].price):
			            temp = products[i]
			            products[i] = products[j]
			            products[j] = temp
	return render_template('products.html', title='products-beanies', products = products, form=form)

#------------------------------------------------------------------------------------

@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html', title='about')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	return render_template('contact.html', title='contact')

@app.route('/basket', methods=['GET', 'POST'])
def basket():
	if not g.customer:
		return redirect(url_for('account'))
	productsinbasket = []
	for i in range (0, len(session['basketcontent'])):
		product = models.Products.query.filter_by(productid=session['basketcontent'][i]).all()
		productsinbasket.append(product[0])
	if request.method == "POST": #if the button to remove a item is pressed
		# Find the button that was pressed
		foundID = request.form.get("remove") #find the id of the button pressed
		# Change the database back appropriately
		p = models.Products.query.get(session['basketcontent'][int(foundID)]) #finds the row in the database
		if session['sizes'][int(foundID)] == 'Extra Small (XS)':
			p.xsstocklevel = p.xsstocklevel + 1
			db.session.commit() #adds to the database
		if session['sizes'][int(foundID)] == 'Small (S)':
			p.sstocklevel = p.sstocklevel + 1
			db.session.commit() #adds to the database
		if session['sizes'][int(foundID)] == 'Medium (M)':
			p.mstocklevel = p.mstocklevel + 1
			db.session.commit() #adds to the database
		if session['sizes'][int(foundID)] == 'Large (L)':
			p.lstocklevel = p.lstocklevel + 1
			db.session.commit() #adds to the database
		if session['sizes'][int(foundID)] == 'Extra Large (XL)':
			p.xlstocklevel = p.xlstocklevel + 1
			db.session.commit() #adds to the database
		# remove from the basket and the sizes (to act like its been deleted from the basket)
		session['basketcontent'].remove(session['basketcontent'][int(foundID)])
		session['sizes'].remove(session['sizes'][int(foundID)])
		session.modified = True
		return redirect(url_for('basket'))
	return render_template('basket.html', title='basket', products = productsinbasket,
							basketsize = len(productsinbasket),sizes = session['sizes'])

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	productsinbasket = []
	for i in range (0, len(session['basketcontent'])):
		product = models.Products.query.filter_by(productid=session['basketcontent'][i]).all()
		productsinbasket.append(product[0])
	if request.method == "POST":
		for i in range (0,len(session['basketcontent'])):
			product = models.Products.query.get(session['basketcontent'][i])
			print(g.customer.purchases)
			g.customer.purchases.append(product)
			print(g.customer.purchases)
			db.session.commit() #commits to the database
			print(g.customer.purchases)
		session['basketcontent'] = []
		session['sizes'] = []
		flash("Purchase complete")
		return redirect(url_for('account'))
	return render_template('checkout.html', title='checkout', products = productsinbasket,
							basketsize = len(productsinbasket),sizes = session['sizes'])

# ---------------------------------- All of the product detail pages -----------------------------------------

@app.route('/product-details-id=1', methods=['GET', 'POST'])
def productdetails1():
	form = PickSize.new()
	product = models.Products.query.filter_by(productid=1).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails1'))
	return render_template('product-details.html', title='product-details-id=1', product = product, form = form)

@app.route('/product-details-id=2', methods=['GET', 'POST'])
def productdetails2():
	form = PickSize2.new()
	product = models.Products.query.filter_by(productid=2).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails2'))
	return render_template('product-details.html', title='product-details-id=2', product = product, form = form)

@app.route('/product-details-id=3', methods=['GET', 'POST'])
def productdetails3():
	form = PickSize3.new()
	product = models.Products.query.filter_by(productid=3).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails3'))
	return render_template('product-details.html', title='product-details-id=3', product = product, form = form)

@app.route('/product-details-id=4', methods=['GET', 'POST'])
def productdetails4():
	form = PickSize4.new()
	product = models.Products.query.filter_by(productid=4).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails4'))
	return render_template('product-details.html', title='product-details-id=4', product = product, form = form)

@app.route('/product-details-id=5', methods=['GET', 'POST'])
def productdetails5():
	form = PickSize5.new()
	product = models.Products.query.filter_by(productid=5).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails5'))
	return render_template('product-details.html', title='product-details-id=5', product = product, form = form)

@app.route('/product-details-id=6', methods=['GET', 'POST'])
def productdetails6():
	form = PickSize6.new()
	product = models.Products.query.filter_by(productid=6).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails6'))
	return render_template('product-details.html', title='product-details-id=6', product = product, form = form)

@app.route('/product-details-id=7', methods=['GET', 'POST'])
def productdetails7():
	form = PickSize7.new()
	product = models.Products.query.filter_by(productid=7).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails7'))
	return render_template('product-details.html', title='product-details-id=7', product = product, form = form)

@app.route('/product-details-id=8', methods=['GET', 'POST'])
def productdetails8():
	form = PickSize8.new()
	product = models.Products.query.filter_by(productid=8).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails8'))
	return render_template('product-details.html', title='product-details-id=8', product = product, form = form)

@app.route('/product-details-id=9', methods=['GET', 'POST'])
def productdetails9():
	form = PickSize9.new()
	product = models.Products.query.filter_by(productid=9).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails9'))
	return render_template('product-details.html', title='product-details-id=9', product = product, form = form)

@app.route('/product-details-id=10', methods=['GET', 'POST'])
def productdetails10():
	form = PickSize10.new()
	product = models.Products.query.filter_by(productid=10).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails10'))
	return render_template('product-details.html', title='product-details-id=10', product = product, form = form)

@app.route('/product-details-id=11', methods=['GET', 'POST'])
def productdetails11():
	form = PickSize11.new()
	product = models.Products.query.filter_by(productid=11).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails11'))
	return render_template('product-details.html', title='product-details-id=11', product = product, form = form)

@app.route('/product-details-id=12', methods=['GET', 'POST'])
def productdetails12():
	form = PickSize12.new()
	product = models.Products.query.filter_by(productid=12).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails12'))
	return render_template('product-details.html', title='product-details-id=12', product = product, form = form)

@app.route('/product-details-id=13', methods=['GET', 'POST'])
def productdetails13():
	form = PickSize13.new()
	product = models.Products.query.filter_by(productid=13).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails13'))
	return render_template('product-details.html', title='product-details-id=13', product = product, form = form)

@app.route('/product-details-id=14', methods=['GET', 'POST'])
def productdetails14():
	form = PickSize14.new()
	product = models.Products.query.filter_by(productid=14).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails14'))
	return render_template('product-details.html', title='product-details-id=14', product = product, form = form)

@app.route('/product-details-id=15', methods=['GET', 'POST'])
def productdetails15():
	form = PickSize15.new()
	product = models.Products.query.filter_by(productid=15).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails15'))
	return render_template('product-details.html', title='product-details-id=15', product = product, form = form)

@app.route('/product-details-id=16', methods=['GET', 'POST'])
def productdetails16():
	form = PickSize16.new()
	product = models.Products.query.filter_by(productid=16).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails16'))
	return render_template('product-details.html', title='product-details-id=16', product = product, form = form)

@app.route('/product-details-id=17', methods=['GET', 'POST'])
def productdetails17():
	form = PickSize17.new()
	product = models.Products.query.filter_by(productid=17).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails17'))
	return render_template('product-details.html', title='product-details-id=17', product = product, form = form)

@app.route('/product-details-id=18', methods=['GET', 'POST'])
def productdetails18():
	form = PickSize18.new()
	product = models.Products.query.filter_by(productid=18).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails18'))
	return render_template('product-details.html', title='product-details-id=18', product = product, form = form)

@app.route('/product-details-id=19', methods=['GET', 'POST'])
def productdetails19():
	form = PickSize19.new()
	product = models.Products.query.filter_by(productid=19).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails19'))
	return render_template('product-details.html', title='product-details-id=19', product = product, form = form)

@app.route('/product-details-id=20', methods=['GET', 'POST'])
def productdetails20():
	form = PickSize20.new()
	product = models.Products.query.filter_by(productid=20).all()
	if request.method == 'POST':
		if not g.customer:
			return redirect(url_for('account'))
		if g.customer:
			session['basketcontent'].append(product[0].productid)
			session.modified = True
			session['sizes'].append(form.size.data)
			p = models.Products.query.get(product[0].productid) #finds the row in the database
			if form.size.data == 'Extra Small (XS)':
				p.xsstocklevel = p.xsstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Small (S)':
				p.sstocklevel = p.sstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Medium (M)':
				p.mstocklevel = p.mstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Large (L)':
				p.lstocklevel = p.lstocklevel - 1
				db.session.commit() #adds to the database
			if form.size.data == 'Extra Large (XL)':
				p.xlstocklevel = p.xlstocklevel - 1
				db.session.commit() #adds to the database
			flash("Item added to basket")
			return redirect(url_for('productdetails20'))
	return render_template('product-details.html', title='product-details-id=20', product = product, form = form)
