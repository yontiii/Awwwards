from django.test import TestCase
from .models import Profile,Projects,Rates


class ProfileTestClass(TestCase):
    def setUp(self):
        self.wanjiku = Profile( profile_photo='default.jpg',bio='heey its me', website='www.john.me', phone_number='0797803412')

    def test_instance(self):
        self.assertTrue(isinstance(self.wanjiku,Profile))

    def test_save(self):
        self.wanjiku.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)
 

 class PostsTestClass(TestCase):
    def setUp(self):
        self.wanjiku = Profile(first_name = 'Wanjiku',last_name='Kariuki',username='ciku_k',email='sheekokariuki@gmail.com')
        self.wanjiku.save_profile()

        self.new_tag=tag(tag='testing')
        self.new_tag.save()

        self.new_post =Posts(caption="testing testing 1,2",profile=self.wanjiku)
        self.new_post.save()

        self.new_post.tag.add(self.new_tag)

    def tearDown(self):
        Profile.objects.all().delete()
        tag.objects.all().delete()
        Posts.objects.all().delete()    

    def test_posts(self):
        posts = Posts.posts()
        self.assertTrue(len(posts)>0)


class RatesTestClass(TestCase):
    def setUp(self):
        self.user = User(username='john',email='john@gmail.com',password='12345')
        
        self.rate = Rates(design=10,usability=10,content=10,user=self.user,project=10)
        self.rate.save()
        
        self.assertTrue(isinstance(self.rate,Rate))        
