from django.db import connection


class SequenceMixin(object):
    default_seq_val = None

    @property
    def seq_name(self):
        if self.id is None:
            raise ValueError
        return "{model_name}_{id}_seq".format(
            id=self.id,
            model_name=self.__class__.__name__.lower()
        )

    @property
    def has_seq(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pg_class
            WHERE relname = '{seq_name}';""".format(
                seq_name=self.seq_name))
        return bool(cursor.fetchone()[0])

    def create_seq(
            self, increment=1, min_value=1,
            max_value=9223372036854775807, start=1, cache=1):
        if not self.has_seq:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE SEQUENCE public.{seq_name}
                    INCREMENT {increment}
                    MINVALUE {min_value}
                    MAXVALUE {max_value}
                    START {start}
                    CACHE {cache};
                ALTER TABLE public.{seq_name}
                    OWNER TO {owner};""".format(
                    seq_name=self.seq_name,
                    increment=increment,
                    min_value=min_value,
                    max_value=max_value,
                    start=start,
                    cache=cache,
                    owner=connection.settings_dict["USER"]))

    def drop_seq(self):
        if self.has_seq:
            cursor = connection.cursor()
            cursor.execute(
                "DROP SEQUENCE public.{seq_name};".format(
                    seq_name=self.seq_name))

    def setval(self, val=1, is_called=True):
        if not self.has_seq:
            self.reset_seq()
        val = int(val)
        is_called = bool(is_called)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SETVAL('%s', %s, %s)" % (
                self.seq_name, val, is_called))
        return cursor.fetchone()[0]

    def nextval(self):
        if not self.has_seq:
            self.reset_seq()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT NEXTVAL('%s')" % (
                self.seq_name))
        return cursor.fetchone()[0]

    def reset_seq(self):
        val = self.get_default_seq_val()
        self.create_seq()
        self.setval(val, False)

    def get_default_seq_val(self):
        if self.default_seq_val is not None:
            return self.default_seq_val
        return 1

