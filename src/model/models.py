"""
Auto generated models from postgres db schema using sqlacodegen
https://pypi.org/project/sqlacodegen/

Extend all models with model.common.ModelMixins
"""

from model.common import ModelMixins


# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_attribute_definition = Table(
    'attribute_definition', metadata,
    Column('attribute_definition_id', Integer, nullable=False),
    Column('attribute_name', String(255), nullable=False),
    Column('attribute_description', Text),
    Column('attribute_type_concept_id', Integer, nullable=False),
    Column('attribute_syntax', Text)
)


class CareSite(Base, ModelMixins):
    __tablename__ = 'care_site'

    care_site_id = Column(BigInteger, primary_key=True)
    care_site_name = Column(String(255))
    place_of_service_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    location_id = Column(ForeignKey('location.location_id'))
    care_site_source_value = Column(String(50))
    place_of_service_source_value = Column(String(50))

    location = relationship('Location')
    place_of_service_concept = relationship('Concept')


t_cdm_source = Table(
    'cdm_source', metadata,
    Column('cdm_source_name', String(255), nullable=False),
    Column('cdm_source_abbreviation', String(25)),
    Column('cdm_holder', String(255)),
    Column('source_description', Text),
    Column('source_documentation_reference', String(255)),
    Column('cdm_etl_reference', String(255)),
    Column('source_release_date', Date),
    Column('cdm_release_date', Date),
    Column('cdm_version', String(10)),
    Column('vocabulary_version', String(20))
)


class Concept(Base, ModelMixins):
    __tablename__ = 'concept'
    __table_args__ = (
        CheckConstraint("(COALESCE(invalid_reason, 'D'::character varying))::text = ANY ((ARRAY['D'::character varying, 'U'::character varying])::text[])"),
        CheckConstraint("(COALESCE(standard_concept, 'C'::character varying))::text = ANY ((ARRAY['C'::character varying, 'S'::character varying])::text[])"),
        CheckConstraint("(concept_code)::text <> ''::text"),
        CheckConstraint("(concept_name)::text <> ''::text")
    )

    concept_id = Column(Integer, primary_key=True, unique=True)
    concept_name = Column(String(255), nullable=False)
    domain_id = Column(ForeignKey('domain.domain_id'), nullable=False, index=True)
    vocabulary_id = Column(ForeignKey('vocabulary.vocabulary_id'), nullable=False, index=True)
    concept_class_id = Column(ForeignKey('concept_class.concept_class_id'), nullable=False, index=True)
    standard_concept = Column(String(1))
    concept_code = Column(String(50), nullable=False, index=True)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    invalid_reason = Column(String(1))

    concept_class = relationship('ConceptClass', primaryjoin='Concept.concept_class_id == ConceptClass.concept_class_id')
    domain = relationship('Domain', primaryjoin='Concept.domain_id == Domain.domain_id')
    vocabulary = relationship('Vocabulary', primaryjoin='Concept.vocabulary_id == Vocabulary.vocabulary_id')


class ConceptAncestor(Base, ModelMixins):
    __tablename__ = 'concept_ancestor'

    ancestor_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    descendant_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    min_levels_of_separation = Column(Integer, nullable=False)
    max_levels_of_separation = Column(Integer, nullable=False)

    ancestor_concept = relationship('Concept', primaryjoin='ConceptAncestor.ancestor_concept_id == Concept.concept_id')
    descendant_concept = relationship('Concept', primaryjoin='ConceptAncestor.descendant_concept_id == Concept.concept_id')


class ConceptClass(Base, ModelMixins):
    __tablename__ = 'concept_class'

    concept_class_id = Column(String(20), primary_key=True, unique=True)
    concept_class_name = Column(String(255), nullable=False)
    concept_class_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    concept_class_concept = relationship('Concept', primaryjoin='ConceptClass.concept_class_concept_id == Concept.concept_id')


class ConceptRelationship(Base, ModelMixins):
    __tablename__ = 'concept_relationship'
    __table_args__ = (
        CheckConstraint("(COALESCE(invalid_reason, 'D'::character varying))::text = 'D'::text"),
    )

    concept_id_1 = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    concept_id_2 = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    relationship_id = Column(ForeignKey('relationship.relationship_id'), primary_key=True, nullable=False, index=True)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    invalid_reason = Column(String(1))

    concept = relationship('Concept', primaryjoin='ConceptRelationship.concept_id_1 == Concept.concept_id')
    concept1 = relationship('Concept', primaryjoin='ConceptRelationship.concept_id_2 == Concept.concept_id')
    relationship = relationship('Relationship')


t_concept_synonym = Table(
    'concept_synonym', metadata,
    Column('concept_id', ForeignKey('concept.concept_id'), nullable=False, index=True),
    Column('concept_synonym_name', String(1000), nullable=False),
    Column('language_concept_id', Integer, nullable=False),
    CheckConstraint("(concept_synonym_name)::text <> ''::text"),
    UniqueConstraint('concept_id', 'concept_synonym_name', 'language_concept_id')
)


class ConditionEra(Base, ModelMixins):
    __tablename__ = 'condition_era'

    condition_era_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    condition_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    condition_era_start_datetime = Column(DateTime, nullable=False)
    condition_era_end_datetime = Column(DateTime, nullable=False)
    condition_occurrence_count = Column(Integer)

    condition_concept = relationship('Concept')
    person = relationship('Person')


class ConditionOccurrence(Base, ModelMixins):
    __tablename__ = 'condition_occurrence'

    condition_occurrence_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    condition_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    condition_start_date = Column(Date)
    condition_start_datetime = Column(DateTime, nullable=False)
    condition_end_date = Column(Date)
    condition_end_datetime = Column(DateTime)
    condition_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    condition_status_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    stop_reason = Column(String(20))
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    condition_source_value = Column(String(50))
    condition_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    condition_status_source_value = Column(String(50))

    condition_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_concept_id == Concept.concept_id')
    condition_source_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_source_concept_id == Concept.concept_id')
    condition_status_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_status_concept_id == Concept.concept_id')
    condition_type_concept = relationship('Concept', primaryjoin='ConditionOccurrence.condition_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


class Cost(Base, ModelMixins):
    __tablename__ = 'cost'

    cost_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    cost_event_id = Column(BigInteger, nullable=False)
    cost_event_field_concept_id = Column(Integer, nullable=False)
    cost_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    cost_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    currency_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    cost = Column(Numeric)
    incurred_date = Column(Date, nullable=False)
    billed_date = Column(Date)
    paid_date = Column(Date)
    revenue_code_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    drg_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    cost_source_value = Column(String(50))
    cost_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    revenue_code_source_value = Column(String(50))
    drg_source_value = Column(String(3))
    payer_plan_period_id = Column(ForeignKey('payer_plan_period.payer_plan_period_id'))

    cost_concept = relationship('Concept', primaryjoin='Cost.cost_concept_id == Concept.concept_id')
    cost_source_concept = relationship('Concept', primaryjoin='Cost.cost_source_concept_id == Concept.concept_id')
    cost_type_concept = relationship('Concept', primaryjoin='Cost.cost_type_concept_id == Concept.concept_id')
    currency_concept = relationship('Concept', primaryjoin='Cost.currency_concept_id == Concept.concept_id')
    drg_concept = relationship('Concept', primaryjoin='Cost.drg_concept_id == Concept.concept_id')
    payer_plan_period = relationship('PayerPlanPeriod')
    person = relationship('Person')
    revenue_code_concept = relationship('Concept', primaryjoin='Cost.revenue_code_concept_id == Concept.concept_id')


class DeviceExposure(Base, ModelMixins):
    __tablename__ = 'device_exposure'

    device_exposure_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    device_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    device_exposure_start_date = Column(Date)
    device_exposure_start_datetime = Column(DateTime, nullable=False)
    device_exposure_end_date = Column(Date)
    device_exposure_end_datetime = Column(DateTime)
    device_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    unique_device_id = Column(String(50))
    quantity = Column(Integer)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    device_source_value = Column(String(100))
    device_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    device_concept = relationship('Concept', primaryjoin='DeviceExposure.device_concept_id == Concept.concept_id')
    device_source_concept = relationship('Concept', primaryjoin='DeviceExposure.device_source_concept_id == Concept.concept_id')
    device_type_concept = relationship('Concept', primaryjoin='DeviceExposure.device_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


class Domain(Base, ModelMixins):
    __tablename__ = 'domain'

    domain_id = Column(String(20), primary_key=True, unique=True)
    domain_name = Column(String(255), nullable=False)
    domain_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    domain_concept = relationship('Concept', primaryjoin='Domain.domain_concept_id == Concept.concept_id')


class DoseEra(Base, ModelMixins):
    __tablename__ = 'dose_era'

    dose_era_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    drug_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    unit_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    dose_value = Column(Numeric, nullable=False)
    dose_era_start_datetime = Column(DateTime, nullable=False)
    dose_era_end_datetime = Column(DateTime, nullable=False)

    drug_concept = relationship('Concept', primaryjoin='DoseEra.drug_concept_id == Concept.concept_id')
    person = relationship('Person')
    unit_concept = relationship('Concept', primaryjoin='DoseEra.unit_concept_id == Concept.concept_id')


class DrugEra(Base, ModelMixins):
    __tablename__ = 'drug_era'

    drug_era_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    drug_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    drug_era_start_datetime = Column(DateTime, nullable=False)
    drug_era_end_datetime = Column(DateTime, nullable=False)
    drug_exposure_count = Column(Integer)
    gap_days = Column(Integer)

    drug_concept = relationship('Concept')
    person = relationship('Person')


class DrugExposure(Base, ModelMixins):
    __tablename__ = 'drug_exposure'

    drug_exposure_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    drug_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    drug_exposure_start_date = Column(Date)
    drug_exposure_start_datetime = Column(DateTime, nullable=False)
    drug_exposure_end_date = Column(Date)
    drug_exposure_end_datetime = Column(DateTime, nullable=False)
    verbatim_end_date = Column(Date)
    drug_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    stop_reason = Column(String(20))
    refills = Column(Integer)
    quantity = Column(Numeric)
    days_supply = Column(Integer)
    sig = Column(Text)
    route_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    lot_number = Column(String(50))
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    drug_source_value = Column(String(50))
    drug_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    route_source_value = Column(String(50))
    dose_unit_source_value = Column(String(50))

    drug_concept = relationship('Concept', primaryjoin='DrugExposure.drug_concept_id == Concept.concept_id')
    drug_source_concept = relationship('Concept', primaryjoin='DrugExposure.drug_source_concept_id == Concept.concept_id')
    drug_type_concept = relationship('Concept', primaryjoin='DrugExposure.drug_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    route_concept = relationship('Concept', primaryjoin='DrugExposure.route_concept_id == Concept.concept_id')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


class DrugStrength(Base, ModelMixins):
    __tablename__ = 'drug_strength'

    drug_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    ingredient_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    amount_value = Column(Numeric)
    amount_unit_concept_id = Column(ForeignKey('concept.concept_id'))
    numerator_value = Column(Numeric)
    numerator_unit_concept_id = Column(ForeignKey('concept.concept_id'))
    denominator_value = Column(Numeric)
    denominator_unit_concept_id = Column(ForeignKey('concept.concept_id'))
    box_size = Column(Integer)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    invalid_reason = Column(String(1))

    amount_unit_concept = relationship('Concept', primaryjoin='DrugStrength.amount_unit_concept_id == Concept.concept_id')
    denominator_unit_concept = relationship('Concept', primaryjoin='DrugStrength.denominator_unit_concept_id == Concept.concept_id')
    drug_concept = relationship('Concept', primaryjoin='DrugStrength.drug_concept_id == Concept.concept_id')
    ingredient_concept = relationship('Concept', primaryjoin='DrugStrength.ingredient_concept_id == Concept.concept_id')
    numerator_unit_concept = relationship('Concept', primaryjoin='DrugStrength.numerator_unit_concept_id == Concept.concept_id')


t_fact_relationship = Table(
    'fact_relationship', metadata,
    Column('domain_concept_id_1', ForeignKey('concept.concept_id'), nullable=False, index=True),
    Column('fact_id_1', BigInteger, nullable=False),
    Column('domain_concept_id_2', ForeignKey('concept.concept_id'), nullable=False, index=True),
    Column('fact_id_2', BigInteger, nullable=False),
    Column('relationship_concept_id', ForeignKey('concept.concept_id'), nullable=False, index=True)
)


class Location(Base, ModelMixins):
    __tablename__ = 'location'

    location_id = Column(BigInteger, primary_key=True)
    address_1 = Column(String(50))
    address_2 = Column(String(50))
    city = Column(String(50))
    state = Column(String(2))
    zip = Column(String(9))
    county = Column(String(20))
    country = Column(String(100))
    location_source_value = Column(String(50))
    latitude = Column(Numeric)
    longitude = Column(Numeric)


class LocationHistory(Base, ModelMixins):
    __tablename__ = 'location_history'

    location_history_id = Column(BigInteger, primary_key=True)
    location_id = Column(ForeignKey('location.location_id'), nullable=False)
    relationship_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    domain_id = Column(String(50), nullable=False)
    entity_id = Column(BigInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)

    location = relationship('Location')
    relationship_type_concept = relationship('Concept')


class Measurement(Base, ModelMixins):
    __tablename__ = 'measurement'

    measurement_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    measurement_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    measurement_date = Column(Date)
    measurement_datetime = Column(DateTime, nullable=False)
    measurement_time = Column(String(10))
    measurement_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    operator_concept_id = Column(ForeignKey('concept.concept_id'))
    value_as_number = Column(Numeric)
    value_as_concept_id = Column(ForeignKey('concept.concept_id'))
    unit_concept_id = Column(ForeignKey('concept.concept_id'))
    range_low = Column(Numeric)
    range_high = Column(Numeric)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    measurement_source_value = Column(String(50))
    measurement_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    unit_source_value = Column(String(50))
    value_source_value = Column(String(50))

    measurement_concept = relationship('Concept', primaryjoin='Measurement.measurement_concept_id == Concept.concept_id')
    measurement_source_concept = relationship('Concept', primaryjoin='Measurement.measurement_source_concept_id == Concept.concept_id')
    measurement_type_concept = relationship('Concept', primaryjoin='Measurement.measurement_type_concept_id == Concept.concept_id')
    operator_concept = relationship('Concept', primaryjoin='Measurement.operator_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    unit_concept = relationship('Concept', primaryjoin='Measurement.unit_concept_id == Concept.concept_id')
    value_as_concept = relationship('Concept', primaryjoin='Measurement.value_as_concept_id == Concept.concept_id')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


t_metadata = Table(
    'metadata', metadata,
    Column('metadata_concept_id', ForeignKey('concept.concept_id'), nullable=False),
    Column('metadata_type_concept_id', ForeignKey('concept.concept_id'), nullable=False),
    Column('name', String(250), nullable=False),
    Column('value_as_string', Text),
    Column('value_as_concept_id', Integer),
    Column('metadata_date', Date),
    Column('metadata_datetime', DateTime)
)


class Note(Base, ModelMixins):
    __tablename__ = 'note'

    note_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    note_event_id = Column(BigInteger)
    note_event_field_concept_id = Column(Integer, nullable=False)
    note_date = Column(Date)
    note_datetime = Column(DateTime, nullable=False)
    note_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    note_class_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    note_title = Column(String(250))
    note_text = Column(Text)
    encoding_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    language_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    note_source_value = Column(String(50))

    encoding_concept = relationship('Concept', primaryjoin='Note.encoding_concept_id == Concept.concept_id')
    language_concept = relationship('Concept', primaryjoin='Note.language_concept_id == Concept.concept_id')
    note_class_concept = relationship('Concept', primaryjoin='Note.note_class_concept_id == Concept.concept_id')
    note_type_concept = relationship('Concept', primaryjoin='Note.note_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


class NoteNlp(Base, ModelMixins):
    __tablename__ = 'note_nlp'

    note_nlp_id = Column(BigInteger, primary_key=True)
    note_id = Column(ForeignKey('note.note_id'), nullable=False, index=True)
    section_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    snippet = Column(String(250))
    offset = Column(String(250))
    lexical_variant = Column(String(250), nullable=False)
    note_nlp_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    nlp_system = Column(String(250))
    nlp_date = Column(Date, nullable=False)
    nlp_datetime = Column(DateTime)
    term_exists = Column(String(1))
    term_temporal = Column(String(50))
    term_modifiers = Column(String(2000))
    note_nlp_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    note = relationship('Note')
    note_nlp_concept = relationship('Concept', primaryjoin='NoteNlp.note_nlp_concept_id == Concept.concept_id')
    note_nlp_source_concept = relationship('Concept', primaryjoin='NoteNlp.note_nlp_source_concept_id == Concept.concept_id')
    section_concept = relationship('Concept', primaryjoin='NoteNlp.section_concept_id == Concept.concept_id')


class Observation(Base, ModelMixins):
    __tablename__ = 'observation'

    observation_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    observation_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    observation_date = Column(Date)
    observation_datetime = Column(DateTime, nullable=False)
    observation_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    value_as_number = Column(Numeric)
    value_as_string = Column(String(60))
    value_as_concept_id = Column(ForeignKey('concept.concept_id'))
    qualifier_concept_id = Column(ForeignKey('concept.concept_id'))
    unit_concept_id = Column(ForeignKey('concept.concept_id'))
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    observation_source_value = Column(String(50))
    observation_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    unit_source_value = Column(String(50))
    qualifier_source_value = Column(String(50))
    observation_event_id = Column(BigInteger)
    obs_event_field_concept_id = Column(Integer, nullable=False)
    value_as_datetime = Column(DateTime)

    observation_concept = relationship('Concept', primaryjoin='Observation.observation_concept_id == Concept.concept_id')
    observation_source_concept = relationship('Concept', primaryjoin='Observation.observation_source_concept_id == Concept.concept_id')
    observation_type_concept = relationship('Concept', primaryjoin='Observation.observation_type_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    qualifier_concept = relationship('Concept', primaryjoin='Observation.qualifier_concept_id == Concept.concept_id')
    unit_concept = relationship('Concept', primaryjoin='Observation.unit_concept_id == Concept.concept_id')
    value_as_concept = relationship('Concept', primaryjoin='Observation.value_as_concept_id == Concept.concept_id')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


class ObservationPeriod(Base, ModelMixins):
    __tablename__ = 'observation_period'

    observation_period_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    observation_period_start_date = Column(Date, nullable=False)
    observation_period_end_date = Column(Date, nullable=False)
    period_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    period_type_concept = relationship('Concept')
    person = relationship('Person')


class PayerPlanPeriod(Base, ModelMixins):
    __tablename__ = 'payer_plan_period'

    payer_plan_period_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    contract_person_id = Column(ForeignKey('person.person_id'))
    payer_plan_period_start_date = Column(Date, nullable=False)
    payer_plan_period_end_date = Column(Date, nullable=False)
    payer_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    plan_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    contract_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    sponsor_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    stop_reason_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    payer_source_value = Column(String(50))
    payer_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    plan_source_value = Column(String(50))
    plan_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    contract_source_value = Column(String(50))
    contract_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    sponsor_source_value = Column(String(50))
    sponsor_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    family_source_value = Column(String(50))
    stop_reason_source_value = Column(String(50))
    stop_reason_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    contract_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.contract_concept_id == Concept.concept_id')
    contract_person = relationship('Person', primaryjoin='PayerPlanPeriod.contract_person_id == Person.person_id')
    contract_source_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.contract_source_concept_id == Concept.concept_id')
    payer_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.payer_concept_id == Concept.concept_id')
    payer_source_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.payer_source_concept_id == Concept.concept_id')
    person = relationship('Person', primaryjoin='PayerPlanPeriod.person_id == Person.person_id')
    plan_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.plan_concept_id == Concept.concept_id')
    plan_source_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.plan_source_concept_id == Concept.concept_id')
    sponsor_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.sponsor_concept_id == Concept.concept_id')
    sponsor_source_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.sponsor_source_concept_id == Concept.concept_id')
    stop_reason_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.stop_reason_concept_id == Concept.concept_id')
    stop_reason_source_concept = relationship('Concept', primaryjoin='PayerPlanPeriod.stop_reason_source_concept_id == Concept.concept_id')


class Person(Base, ModelMixins):
    __tablename__ = 'person'

    person_id = Column(BigInteger, primary_key=True, unique=True)
    gender_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    month_of_birth = Column(Integer)
    day_of_birth = Column(Integer)
    birth_datetime = Column(DateTime)
    death_datetime = Column(DateTime)
    race_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    ethnicity_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    location_id = Column(ForeignKey('location.location_id'))
    provider_id = Column(ForeignKey('provider.provider_id'))
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    person_source_value = Column(String(50))
    gender_source_value = Column(String(50))
    gender_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    race_source_value = Column(String(50))
    race_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    ethnicity_source_value = Column(String(50))
    ethnicity_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    care_site = relationship('CareSite')
    ethnicity_concept = relationship('Concept', primaryjoin='Person.ethnicity_concept_id == Concept.concept_id')
    ethnicity_source_concept = relationship('Concept', primaryjoin='Person.ethnicity_source_concept_id == Concept.concept_id')
    gender_concept = relationship('Concept', primaryjoin='Person.gender_concept_id == Concept.concept_id')
    gender_source_concept = relationship('Concept', primaryjoin='Person.gender_source_concept_id == Concept.concept_id')
    location = relationship('Location')
    provider = relationship('Provider')
    race_concept = relationship('Concept', primaryjoin='Person.race_concept_id == Concept.concept_id')
    race_source_concept = relationship('Concept', primaryjoin='Person.race_source_concept_id == Concept.concept_id')


class ProcedureOccurrence(Base, ModelMixins):
    __tablename__ = 'procedure_occurrence'

    procedure_occurrence_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    procedure_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    procedure_date = Column(Date)
    procedure_datetime = Column(DateTime, nullable=False)
    procedure_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    modifier_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    quantity = Column(Integer)
    provider_id = Column(ForeignKey('provider.provider_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), index=True)
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    procedure_source_value = Column(String(50))
    procedure_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    modifier_source_value = Column(String(50))

    modifier_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.modifier_concept_id == Concept.concept_id')
    person = relationship('Person')
    procedure_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.procedure_concept_id == Concept.concept_id')
    procedure_source_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.procedure_source_concept_id == Concept.concept_id')
    procedure_type_concept = relationship('Concept', primaryjoin='ProcedureOccurrence.procedure_type_concept_id == Concept.concept_id')
    provider = relationship('Provider')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence')


class Provider(Base, ModelMixins):
    __tablename__ = 'provider'

    provider_id = Column(BigInteger, primary_key=True)
    provider_name = Column(String(255))
    npi = Column(String(20))
    dea = Column(String(20))
    specialty_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    year_of_birth = Column(Integer)
    gender_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    provider_source_value = Column(String(50))
    specialty_source_value = Column(String(50))
    specialty_source_concept_id = Column(ForeignKey('concept.concept_id'))
    gender_source_value = Column(String(50))
    gender_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    care_site = relationship('CareSite')
    gender_concept = relationship('Concept', primaryjoin='Provider.gender_concept_id == Concept.concept_id')
    gender_source_concept = relationship('Concept', primaryjoin='Provider.gender_source_concept_id == Concept.concept_id')
    specialty_concept = relationship('Concept', primaryjoin='Provider.specialty_concept_id == Concept.concept_id')
    specialty_source_concept = relationship('Concept', primaryjoin='Provider.specialty_source_concept_id == Concept.concept_id')


class Relationship(Base, ModelMixins):
    __tablename__ = 'relationship'

    relationship_id = Column(String(20), primary_key=True, unique=True)
    relationship_name = Column(String(255), nullable=False)
    is_hierarchical = Column(String(1), nullable=False)
    defines_ancestry = Column(String(1), nullable=False)
    reverse_relationship_id = Column(ForeignKey('relationship.relationship_id'), nullable=False)
    relationship_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    relationship_concept = relationship('Concept')
    reverse_relationship = relationship('Relationship', remote_side=[relationship_id])


class SourceToConceptMap(Base, ModelMixins):
    __tablename__ = 'source_to_concept_map'

    source_code = Column(String(50), primary_key=True, nullable=False, index=True)
    source_concept_id = Column(Integer, nullable=False)
    source_vocabulary_id = Column(ForeignKey('vocabulary.vocabulary_id'), primary_key=True, nullable=False, index=True)
    source_code_description = Column(String(255))
    target_concept_id = Column(ForeignKey('concept.concept_id'), primary_key=True, nullable=False, index=True)
    target_vocabulary_id = Column(ForeignKey('vocabulary.vocabulary_id'), nullable=False, index=True)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, primary_key=True, nullable=False)
    invalid_reason = Column(String(1))

    source_vocabulary = relationship('Vocabulary', primaryjoin='SourceToConceptMap.source_vocabulary_id == Vocabulary.vocabulary_id')
    target_concept = relationship('Concept')
    target_vocabulary = relationship('Vocabulary', primaryjoin='SourceToConceptMap.target_vocabulary_id == Vocabulary.vocabulary_id')


class Speciman(Base, ModelMixins):
    __tablename__ = 'specimen'

    specimen_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    specimen_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    specimen_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    specimen_date = Column(Date)
    specimen_datetime = Column(DateTime, nullable=False)
    quantity = Column(Numeric)
    unit_concept_id = Column(ForeignKey('concept.concept_id'))
    anatomic_site_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    disease_status_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    specimen_source_id = Column(String(50))
    specimen_source_value = Column(String(50))
    unit_source_value = Column(String(50))
    anatomic_site_source_value = Column(String(50))
    disease_status_source_value = Column(String(50))

    anatomic_site_concept = relationship('Concept', primaryjoin='Speciman.anatomic_site_concept_id == Concept.concept_id')
    disease_status_concept = relationship('Concept', primaryjoin='Speciman.disease_status_concept_id == Concept.concept_id')
    person = relationship('Person')
    specimen_concept = relationship('Concept', primaryjoin='Speciman.specimen_concept_id == Concept.concept_id')
    specimen_type_concept = relationship('Concept', primaryjoin='Speciman.specimen_type_concept_id == Concept.concept_id')
    unit_concept = relationship('Concept', primaryjoin='Speciman.unit_concept_id == Concept.concept_id')


class SurveyConduct(Base, ModelMixins):
    __tablename__ = 'survey_conduct'

    survey_conduct_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    survey_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    survey_start_date = Column(Date)
    survey_start_datetime = Column(DateTime)
    survey_end_date = Column(Date)
    survey_end_datetime = Column(DateTime, nullable=False)
    provider_id = Column(ForeignKey('provider.provider_id'))
    assisted_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    respondent_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    timing_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    collection_method_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    assisted_source_value = Column(String(50))
    respondent_type_source_value = Column(String(100))
    timing_source_value = Column(String(100))
    collection_method_source_value = Column(String(100))
    survey_source_value = Column(String(100))
    survey_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    survey_source_identifier = Column(String(100))
    validated_survey_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    validated_survey_source_value = Column(String(100))
    survey_version_number = Column(String(20))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'))
    visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    response_visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'))

    assisted_concept = relationship('Concept', primaryjoin='SurveyConduct.assisted_concept_id == Concept.concept_id')
    collection_method_concept = relationship('Concept', primaryjoin='SurveyConduct.collection_method_concept_id == Concept.concept_id')
    person = relationship('Person')
    provider = relationship('Provider')
    respondent_type_concept = relationship('Concept', primaryjoin='SurveyConduct.respondent_type_concept_id == Concept.concept_id')
    response_visit_occurrence = relationship('VisitOccurrence', primaryjoin='SurveyConduct.response_visit_occurrence_id == VisitOccurrence.visit_occurrence_id')
    survey_concept = relationship('Concept', primaryjoin='SurveyConduct.survey_concept_id == Concept.concept_id')
    survey_source_concept = relationship('Concept', primaryjoin='SurveyConduct.survey_source_concept_id == Concept.concept_id')
    timing_concept = relationship('Concept', primaryjoin='SurveyConduct.timing_concept_id == Concept.concept_id')
    validated_survey_concept = relationship('Concept', primaryjoin='SurveyConduct.validated_survey_concept_id == Concept.concept_id')
    visit_detail = relationship('VisitDetail')
    visit_occurrence = relationship('VisitOccurrence', primaryjoin='SurveyConduct.visit_occurrence_id == VisitOccurrence.visit_occurrence_id')


class VisitDetail(Base, ModelMixins):
    __tablename__ = 'visit_detail'

    visit_detail_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    visit_detail_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    visit_detail_start_date = Column(Date)
    visit_detail_start_datetime = Column(DateTime, nullable=False)
    visit_detail_end_date = Column(Date)
    visit_detail_end_datetime = Column(DateTime, nullable=False)
    visit_detail_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    provider_id = Column(ForeignKey('provider.provider_id'))
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    discharge_to_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    admitted_from_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    admitted_from_source_value = Column(String(50))
    visit_detail_source_value = Column(String(50))
    visit_detail_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    discharge_to_source_value = Column(String(50))
    preceding_visit_detail_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    visit_detail_parent_id = Column(ForeignKey('visit_detail.visit_detail_id'))
    visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'), nullable=False)

    admitted_from_concept = relationship('Concept', primaryjoin='VisitDetail.admitted_from_concept_id == Concept.concept_id')
    care_site = relationship('CareSite')
    discharge_to_concept = relationship('Concept', primaryjoin='VisitDetail.discharge_to_concept_id == Concept.concept_id')
    person = relationship('Person')
    preceding_visit_detail = relationship('VisitDetail', remote_side=[visit_detail_id], primaryjoin='VisitDetail.preceding_visit_detail_id == VisitDetail.visit_detail_id')
    provider = relationship('Provider')
    visit_detail_concept = relationship('Concept', primaryjoin='VisitDetail.visit_detail_concept_id == Concept.concept_id')
    visit_detail_parent = relationship('VisitDetail', remote_side=[visit_detail_id], primaryjoin='VisitDetail.visit_detail_parent_id == VisitDetail.visit_detail_id')
    visit_detail_source_concept = relationship('Concept', primaryjoin='VisitDetail.visit_detail_source_concept_id == Concept.concept_id')
    visit_detail_type_concept = relationship('Concept', primaryjoin='VisitDetail.visit_detail_type_concept_id == Concept.concept_id')
    visit_occurrence = relationship('VisitOccurrence')


class VisitOccurrence(Base, ModelMixins):
    __tablename__ = 'visit_occurrence'

    visit_occurrence_id = Column(BigInteger, primary_key=True)
    person_id = Column(ForeignKey('person.person_id'), nullable=False, index=True)
    visit_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False, index=True)
    visit_start_date = Column(Date)
    visit_start_datetime = Column(DateTime, nullable=False)
    visit_end_date = Column(Date)
    visit_end_datetime = Column(DateTime, nullable=False)
    visit_type_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    provider_id = Column(ForeignKey('provider.provider_id'))
    care_site_id = Column(ForeignKey('care_site.care_site_id'))
    visit_source_value = Column(String(50))
    visit_source_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    admitted_from_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    admitted_from_source_value = Column(String(50))
    discharge_to_source_value = Column(String(50))
    discharge_to_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)
    preceding_visit_occurrence_id = Column(ForeignKey('visit_occurrence.visit_occurrence_id'))

    admitted_from_concept = relationship('Concept', primaryjoin='VisitOccurrence.admitted_from_concept_id == Concept.concept_id')
    care_site = relationship('CareSite')
    discharge_to_concept = relationship('Concept', primaryjoin='VisitOccurrence.discharge_to_concept_id == Concept.concept_id')
    person = relationship('Person')
    preceding_visit_occurrence = relationship('VisitOccurrence', remote_side=[visit_occurrence_id])
    provider = relationship('Provider')
    visit_concept = relationship('Concept', primaryjoin='VisitOccurrence.visit_concept_id == Concept.concept_id')
    visit_source_concept = relationship('Concept', primaryjoin='VisitOccurrence.visit_source_concept_id == Concept.concept_id')
    visit_type_concept = relationship('Concept', primaryjoin='VisitOccurrence.visit_type_concept_id == Concept.concept_id')


class Vocabulary(Base, ModelMixins):
    __tablename__ = 'vocabulary'

    vocabulary_id = Column(String(20), primary_key=True, unique=True)
    vocabulary_name = Column(String(255), nullable=False)
    vocabulary_reference = Column(String(255), nullable=False)
    vocabulary_version = Column(String(255))
    vocabulary_concept_id = Column(ForeignKey('concept.concept_id'), nullable=False)

    vocabulary_concept = relationship('Concept', primaryjoin='Vocabulary.vocabulary_concept_id == Concept.concept_id')

