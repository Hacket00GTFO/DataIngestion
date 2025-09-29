"""create tiros tables and enums"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "202403120001"
down_revision = None
branch_labels = None
depends_on = None


GENERO_ENUM = "genero_enum"
MANO_ENUM = "mano_habil_enum"


def upgrade() -> None:
    genero_enum = postgresql.ENUM(
        "Masculino",
        "Femenino",
        "Otro",
        name=GENERO_ENUM,
        create_type=False,
    )
    mano_enum = postgresql.ENUM(
        "Diestro",
        "Zurdo",
        "Ambidiestro",
        name=MANO_ENUM,
        create_type=False,
    )

    genero_enum.create(op.get_bind(), checkfirst=True)
    mano_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tiros_staging",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("nombre_tirador", sa.Text(), nullable=True),
        sa.Column("edad", sa.Text(), nullable=True),
        sa.Column("experiencia", sa.Text(), nullable=True),
        sa.Column("distancia_de_tiro", sa.Text(), nullable=True),
        sa.Column("angulo", sa.Text(), nullable=True),
        sa.Column("altura_de_tirador", sa.Text(), nullable=True),
        sa.Column("peso", sa.Text(), nullable=True),
        sa.Column("ambiente", sa.Text(), nullable=True),
        sa.Column("genero", sa.Text(), nullable=True),
        sa.Column("peso_del_balon", sa.Text(), nullable=True),
        sa.Column("tiempo_de_tiro", sa.Text(), nullable=True),
        sa.Column("tiro_exitoso", sa.Text(), nullable=True),
        sa.Column("diestro_zurdo", sa.Text(), nullable=True),
        sa.Column("calibre_de_balon", sa.Text(), nullable=True),
        schema="public",
    )

    op.create_table(
        "tiros",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("nombre_tirador", sa.String(length=120), nullable=False),
        sa.Column("edad", sa.SmallInteger(), nullable=False),
        sa.Column("experiencia_anios", sa.SmallInteger(), nullable=False),
        sa.Column("distancia_m", sa.Numeric(6, 2), nullable=False),
        sa.Column("angulo_grados", sa.SmallInteger(), nullable=False),
        sa.Column("altura_tirador_m", sa.Numeric(4, 2), nullable=False),
        sa.Column("peso_tirador_kg", sa.Numeric(6, 2), nullable=False),
        sa.Column("ambiente", sa.String(length=60), nullable=True),
        sa.Column("genero", genero_enum, nullable=True),
        sa.Column("peso_balon_g", sa.Integer(), nullable=False),
        sa.Column("tiempo_tiro_s", sa.Numeric(6, 3), nullable=False),
        sa.Column("exitos", sa.Integer(), nullable=False),
        sa.Column("intentos", sa.Integer(), nullable=False),
        sa.Column("mano_habil", mano_enum, nullable=True),
        sa.Column("calibre_balon", sa.SmallInteger(), nullable=True),
        sa.CheckConstraint("edad BETWEEN 5 AND 120", name="ck_tiros_edad_rango"),
        sa.CheckConstraint("experiencia_anios >= 0", name="ck_tiros_experiencia_non_negative"),
        sa.CheckConstraint("distancia_m > 0", name="ck_tiros_distancia_positive"),
        sa.CheckConstraint("angulo_grados BETWEEN 0 AND 360", name="ck_tiros_angulo_rango"),
        sa.CheckConstraint("altura_tirador_m > 0 AND altura_tirador_m < 3.0", name="ck_tiros_altura_rango"),
        sa.CheckConstraint("peso_tirador_kg > 0 AND peso_tirador_kg < 400", name="ck_tiros_peso_rango"),
        sa.CheckConstraint("peso_balon_g > 0", name="ck_tiros_peso_balon_positive"),
        sa.CheckConstraint("tiempo_tiro_s > 0", name="ck_tiros_tiempo_positive"),
        sa.CheckConstraint("exitos >= 0", name="ck_tiros_exitos_non_negative"),
        sa.CheckConstraint("intentos > 0 AND intentos <= 100", name="ck_tiros_intentos_rango"),
        schema="public",
    )

    op.create_index("ix_tiros_nombre_tirador", "tiros", ["nombre_tirador"], unique=False, schema="public")
    op.create_index("ix_tiros_genero", "tiros", ["genero"], unique=False, schema="public")
    op.create_index("ix_tiros_mano_habil", "tiros", ["mano_habil"], unique=False, schema="public")


def downgrade() -> None:
    op.drop_index("ix_tiros_mano_habil", table_name="tiros", schema="public")
    op.drop_index("ix_tiros_genero", table_name="tiros", schema="public")
    op.drop_index("ix_tiros_nombre_tirador", table_name="tiros", schema="public")

    op.drop_table("tiros", schema="public")
    op.drop_table("tiros_staging", schema="public")

    mano_enum = postgresql.ENUM(name=MANO_ENUM)
    genero_enum = postgresql.ENUM(name=GENERO_ENUM)

    mano_enum.drop(op.get_bind(), checkfirst=True)
    genero_enum.drop(op.get_bind(), checkfirst=True)
