from django.urls import path
from .views import add_patient,add_health_info,about,home,chuandoanBN, signIn,signUp,member,send_coze_api_request,chatbot
# ,add_info,edit_info,delete_info,info_list
urlpatterns = [
    path('', home,name='home'),
    path('about/', about, name='about'),
    path('thongtinBN/',add_patient,name='thongtinBN'),
    path('chuandoanBN/',chuandoanBN,name="chuandoanBN"),
    path('member',member,name='member'),
    path('signIn/',signIn,name='signIn'),
    path('signUp/',signUp,name='signUp'),
    # path('chuandoanBN/<int:patient_id>/', chuandoanBN, name='chuandoanBN'),
    path('add_health_info/', add_health_info, name='add_health_info'),
    path('chatbot/', chatbot, name='chatbot'),
    path('send_coze_api_request/', send_coze_api_request, name='send_coze_api_request'),
    # path('chandoan/', add_info, name='add_info'),
    # path('edit/<int:id>/', edit_info, name='edit_info'),
    # path('delete/<int:id>/',delete_info, name='delete_info'),
]