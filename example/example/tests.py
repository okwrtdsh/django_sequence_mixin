from django.db import connection
from django.test import TestCase
from example.models import Mymodel

class SequenceMixinTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m1 = Mymodel.objects.create(
            num=1,
            enabled=True
        )
        cls.m2 = Mymodel.objects.create(
            num=2,
            enabled=True
        )
        cls.m3 = Mymodel.objects.create(
            num=3,
            enabled=True
        )
        cls.m4 = Mymodel.objects.create(
            num=4,
            enabled=True
        )
        cls.m5 = Mymodel.objects.create(
            num=5,
            enabled=True
        )
        cls.m6 = Mymodel.objects.create(
            num=6,
            enabled=True
        )
        cls.m7 = Mymodel.objects.create(
            num=7,
            enabled=True
        )
        cls.m8 = Mymodel.objects.create(
            num=8,
            enabled=True
        )

    def test_seq_name(self):
        self.assertEqual(
            self.m1.seq_name,
            "{model_name}_{id}_seq".format(
                id=self.m1.id,
                model_name=self.m1.__class__.__name__.lower()
            )
        )

    def test_has_seq(self):
        self.assertFalse(self.m2.has_seq)
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE SEQUENCE public.{seq_name}
            INCREMENT 1
            MINVALUE 1
            MAXVALUE 9223372036854775807
            START 1
            CACHE 1;
            ALTER TABLE public.{seq_name}
            OWNER TO {owner};""".format(
                seq_name=self.m2.seq_name,
                owner=connection.settings_dict["USER"]))
        self.assertTrue(self.m2.has_seq)
        cursor.execute(
            "DROP SEQUENCE public.{seq_name};".format(
                seq_name=self.m2.seq_name))
        self.assertFalse(self.m2.has_seq)

    def test_create_seq(self):
        self.assertFalse(self.m3.has_seq)
        self.m3.create_seq()
        self.assertTrue(self.m3.has_seq)
        cursor = connection.cursor()
        cursor.execute(
            "DROP SEQUENCE public.{seq_name};".format(
                seq_name=self.m3.seq_name))
        self.assertFalse(self.m3.has_seq)

    def test_drop_seq(self):
        self.assertFalse(self.m4.has_seq)
        self.m4.create_seq()
        self.assertTrue(self.m4.has_seq)
        self.m4.drop_seq()
        self.assertFalse(self.m4.has_seq)

    def test_nextval(self):
        self.assertFalse(self.m5.has_seq)
        self.m5.create_seq()
        self.assertTrue(self.m5.has_seq)
        self.assertEqual(self.m5.nextval(), 1)
        self.assertEqual(self.m5.nextval(), 2)
        self.m5.drop_seq()
        self.assertFalse(self.m5.has_seq)

    def test_setval(self):
        self.assertFalse(self.m6.has_seq)
        self.m6.create_seq()
        self.assertTrue(self.m6.has_seq)
        self.assertEqual(self.m6.setval(100, False), 100)
        self.assertEqual(self.m6.nextval(), 100)
        self.assertEqual(self.m6.setval(100), 100)
        self.assertEqual(self.m6.nextval(), 101)
        self.m6.drop_seq()
        self.assertFalse(self.m6.has_seq)

    def test_reset_seq(self):
        self.assertFalse(self.m7.has_seq)
        self.m7.reset_seq()
        self.assertTrue(self.m7.has_seq)
        self.assertEqual(self.m7.nextval(), 1)
        self.m7.drop_seq()
        self.assertFalse(self.m7.has_seq)

    def test_get_default_seq_val(self):
        self.assertEqual(self.m8.get_default_seq_val(), 1)
        self.m8.default_seq_val = 5
        self.assertEqual(self.m8.get_default_seq_val(), 5)

