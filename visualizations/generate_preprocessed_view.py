import pandas as pd
import numpy as np
import V001, V002, V003, V004, V005, V006, V007, V008, V009, V010, V011

class PreprocessedView:
    _student_names = []
    
    def __init__(self):
        pass
    
    def random_data(self, n_students=20,names=[]):
        if len(names)==0:
            names = pd.read_csv("assets/names.csv")
            self._student_names = [names.group_name[np.random.randint(0,len(names.group_name)+1)] for n in range(0,n_students)]
        else:
            self._student_names = [names[n] for n in range(0,n_students)]
        self._student_names.sort()

    def generate_view_001(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)
        
        instance = V001.V001()
        instance.generate_dataset(number_assigns=10, rand_names=self._student_names)

        for i in range(1,56):
            instance.save_chart(i)
        
        print('V001 done!')
    
    def generate_view_002(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V002.V002()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,19):
            instance.save_chart(i)
        
        print('V002 done!')

    def generate_view_003(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V003.V003()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,11):
            instance.save_chart(i)
        
        print('V003 done!')

    def generate_view_004(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V004.V004()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,13):
            instance.save_chart(i)
        
        print('V004 done!')

    def generate_view_005(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V005.V005()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,25):
            instance.save_chart(i)
        
        print('V005 done!')

    def generate_view_006(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V006.V006()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,14):
            instance.save_chart(i)
        
        print('V006 done!')

    def generate_view_007(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V007.V007()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,5):
            instance.save_chart(i)
        
        print('V007 done!')
    
    def generate_view_008(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V008.V008()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,14):
            instance.save_chart(i)
        
        print('V008 done!')

    def generate_view_009(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V009.V009()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,6):
            instance.save_chart(i)
        
        print('V009 done!')

    def generate_view_010(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V010.V010()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,33):
            instance.save_chart(i)
        
        print('V010 done!')

    def generate_view_011(self,n_students):
        if len(self._student_names) == 0:
            self.random_data(n_students)

        instance = V011.V011()
        instance.generate_dataset(rand_names=self._student_names)
        
        for i in range(1,6):
            instance.save_chart(i)
        
        print('V011 done!')

    def generate_all_views(self,n_students,names=[]):
        print('Selecting names...')
        self.random_data(n_students,names)
        print('Generating views...')
        self.generate_view_001(n_students)
        self.generate_view_002(n_students)
        self.generate_view_003(n_students)
        self.generate_view_004(n_students)
        self.generate_view_005(n_students)
        self.generate_view_006(n_students)
        self.generate_view_007(n_students)
        self.generate_view_008(n_students)
        self.generate_view_009(n_students)
        self.generate_view_010(n_students)
        self.generate_view_011(n_students)



names = ["Arthur","Enzo" ,"Gabriel","Miguel","Carlos","Heitor","Pedro","Henrique","Jorge","Francisco","Caio","Lucas","Rafael","Samuel","Diego","Alana","Luana","Dandara","Laura","Marcela","Maria","Eduarda","Clara","Alice","Ana","Sandra","Amanda","Camila","Valentina","Joana"]
instance = PreprocessedView()
instance.generate_all_views(len(names),names)