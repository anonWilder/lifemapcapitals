from django.contrib import admin
from django.urls import path
from . import views
# from .views import DashboardView


# app_name = 'items'
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.DashboardView, name="DashboardView"),
    path('transactions/', views.transaction, name="transaction"),
    path('about-us/', views.about, name="about"),
    path('retirement/', views.retirement, name="retirement"),
    path('deposit/', views.deposit, name="deposit"),
    path('referal/', views.referal, name="referal"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('support/', views.support, name="support"),
    path('packages/', views.parkages, name="parkages"),
    path('adminPAR/', views.adminPAR, name="adminPAR"),
    path('adminDT/', views.adminDT, name="adminDT"),
    path('adminWD/', views.adminWD, name="adminWD"),
    path('all_user/', views.all_user, name="all_user"),
    path('subscrib/', views.subscrib, name="subscrib"),
    path('kyc/', views.kyc, name="kyc"),
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),
    path('editpak/<int:id>', views.editpak),
    path('updatepak/<int:id>', views.updatepak), 
    path('delete/<int:id>', views.destroy),
    path('pardestroy/<int:id>/', views.pardestroy, name="pardestroy"),
    path('massage/<int:id>', views.massage),
    path('approvalmail/<int:id>', views.approvalmail),
    path('declinmail/<int:id>', views.declinmail),
    path('packdeclinmail/<int:id>', views.packdeclinmail),
    
    path('deletew/<int:id>', views.destroyw),
    path('collect_payment/btc/form=cloctpa&oq=cloctpa&aqs=chrome..69i57.7541j0j7&sourceid=chrome&ie=UTF-8/', views.collect_payment, name='collect_payment'),
    # path('payments/create/<pk>', views.create_payment, name='create_payment'),
    # path('payment/invoice/<pk>',views.track_invoice, name='track_payment'),
    # path('payments/receive/', views.receive_payment, name='receive_payment'),
    path('createOrders/', views.createOrders, name="createOrders"),
    path('Decreate/', views.Decreate, name="Decreate"),
    
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('update_order1/<str:pk>', views.updateOrder1, name="update_order1"),
    path('update_order2/<str:pk>', views.updateOrder2, name="update_order2"),
    path('update_order3/<str:pk>', views.updateOrder3, name="update_order3"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('speacial_parkages/', views.speacial_parkages, name="speacial_parkages"),
    path('kycmassage/', views.kycmassage, name="kycmassage"),
    path('dont/', views.scedual),
    path('client-ip/', views.clientip),
    path('transaction_first/', views.transaction_first, name="transaction_first"),
    path('terms/', views.terms, name="terms"),
    path('privacy/', views.privacy, name="privacy"),
    path('affiliate/', views.affiliate, name="affiliate"),
    path('auto/', views.auto, name="auto"),
]