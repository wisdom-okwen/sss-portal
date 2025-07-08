from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.organization import OrganizationService
from backend.models.organization import Organization
from backend.database import db_session

api = APIRouter(prefix="/api/organizations")
openapi_tags = {
    "name": "Organizations",
    "description": "Organization management and related operations.",
}


@api.get("", response_model=list[Organization], tags=["Organizations"])
def get_organizations(db: Session = Depends(db_session)) -> list[Organization]:
    """
    Get all organizations

    Parameters:
        db: Database session

    Returns:
        list[Organization]: All `Organization`s in the organization table
    """
    return OrganizationService(db).get_all()


@api.get("/by_slug/{slug}", response_model=Organization, tags=["Organizations"])
def get_organization_by_slug(
    slug: str, db: Session = Depends(db_session)
) -> Organization | None:
    """
    Get an organization by slug

    Parameters:
        slug: Slug of the organization to retrieve
        db: Database session

    Returns:
        Organization | None: The `Organization` with the specified slug, or None if not found
    """
    return OrganizationService(db).get_organization_by_slug(slug)


@api.get("/{organization_id}", response_model=Organization, tags=["Organizations"])
def get_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> Organization | None:
    """
    Get an organization by ID

    Parameters:
        organization_id: ID of the organization to retrieve
        db: Database session

    Returns:
        Organization | None: The `Organization` with the specified ID, or None if not found
    """
    return OrganizationService(db).get_organization_by_id(organization_id)


@api.post("", response_model=Organization, tags=["Organizations"])
def create_organization(
    organization: Organization, db: Session = Depends(db_session)
) -> Organization:
    """
    Create a new organization

    Parameters:
        organization: The organization data to create
        db: Database session

    Returns:
        Organization: The created `Organization`
    """
    return OrganizationService(db).create_organization(organization)


@api.put(
    "/{organization_id}", response_model=Organization | None, tags=["Organizations"]
)
def update_organization(
    organization_id: str, organization: Organization, db: Session = Depends(db_session)
) -> Organization | None:
    """
    Update an existing organization

    Parameters:
        organization_id: ID of the organization to update
        organization: The updated organization data
        db: Database session

    Returns:
        Organization | None: The updated `Organization`, or None if not found
    """
    return OrganizationService(db).update_organization(organization_id, organization)


@api.delete("/{organization_id}", response_model=bool, tags=["Organizations"])
def delete_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> bool:
    """
    Delete an organization by ID

    Parameters:
        organization_id: ID of the organization to delete
        db: Database session

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    return OrganizationService(db).delete_organization(organization_id)


@api.get("/user/{user_id}", response_model=list[Organization], tags=["Organizations"])
def get_organizations_by_user(
    user_id: str, db: Session = Depends(db_session)
) -> list[Organization]:
    """
    Get organizations associated with a user

    Parameters:
        user_id: ID of the user to retrieve organizations for
        db: Database session

    Returns:
        list[Organization]: List of `Organization`s associated with the user
    """
    return OrganizationService(db).get_organizations_by_user(user_id)


@api.get(
    "/{organization_id}/members",
    response_model=list[Organization],
    tags=["Organizations"],
)
def get_members_by_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> list[Organization]:
    """
    Get members of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve members for
        db: Database session

    Returns:
        list[Organization]: List of `Organization`s with their members
    """
    return OrganizationService(db).get_members_by_organization(organization_id)


@api.post(
    "/{organization_id}/members", response_model=Organization, tags=["Organizations"]
)
def add_member_to_organization(
    organization_id: str, user: Organization, db: Session = Depends(db_session)
) -> Organization:
    """
    Add a member to an organization

    Parameters:
        organization_id: ID of the organization to add the member to
        user: The user data to add as a member
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new member added
    """
    return OrganizationService(db).add_member_to_organization(organization_id, user)


@api.delete(
    "/{organization_id}/members/{user_id}", response_model=bool, tags=["Organizations"]
)
def remove_member_from_organization(
    organization_id: str, user_id: str, db: Session = Depends(db_session)
) -> bool:
    """
    Remove a member from an organization

    Parameters:
        organization_id: ID of the organization to remove the member from
        user_id: ID of the user to remove
        db: Database session

    Returns:
        bool: True if removal was successful, False otherwise
    """
    return OrganizationService(db).remove_member_from_organization(
        organization_id, user_id
    )


@api.get(
    "/{organization_id}/admins",
    response_model=list[Organization],
    tags=["Organizations"],
)
def get_admins_by_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> list[Organization]:
    """
    Get admin members of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve admins for
        db: Database session

    Returns:
        list[Organization]: List of `Organization`s with their admin members
    """
    return OrganizationService(db).get_admins_by_organization(organization_id)


@api.get(
    "/{organization_id}/teachers",
    response_model=list[Organization],
    tags=["Organizations"],
)
def get_teachers_by_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> list[Organization]:
    """
    Get teachers of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve teachers for
        db: Database session

    Returns:
        list[Organization]: List of `Organization`s with their teachers
    """
    return OrganizationService(db).get_teachers_by_organization(organization_id)


@api.get(
    "/{organization_id}/executive_members",
    response_model=list[Organization],
    tags=["Organizations"],
)
def get_executive_members_by_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> list[Organization]:
    """
    Get executive members of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve executive members for
        db: Database session

    Returns:
        list[Organization]: List of `Organization`s with their executive members
    """
    return OrganizationService(db).get_executive_members_by_organization(
        organization_id
    )


@api.post(
    "/{organization_id}/admins", response_model=Organization, tags=["Organizations"]
)
def add_admin_to_organization(
    organization_id: str, user: Organization, db: Session = Depends(db_session)
) -> Organization:
    """
    Add an admin to an organization

    Parameters:
        organization_id: ID of the organization to add the admin to
        user: The user data to add as an admin
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new admin added
    """
    return OrganizationService(db).add_admin_to_organization(organization_id, user)


@api.get(
    "/{organization_id}/advisor", response_model=Organization, tags=["Organizations"]
)
def get_advisor_by_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> Organization | None:
    """
    Get the advisor of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve the advisor for
        db: Database session

    Returns:
        Organization | None: The `Organization` with its advisor, or None if not found
    """
    return OrganizationService(db).get_advisor_by_organization(organization_id)


@api.post(
    "/{organization_id}/advisor", response_model=Organization, tags=["Organizations"]
)
def add_advisor_to_organization(
    organization_id: str, user: Organization, db: Session = Depends(db_session)
) -> Organization:
    """
    Add an advisor to an organization

    Parameters:
        organization_id: ID of the organization to add the advisor to
        user: The user data to add as an advisor
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new advisor added
    """
    return OrganizationService(db).set_advisor_for_organization(organization_id, user)


@api.delete("/{organization_id}/advisor", response_model=bool, tags=["Organizations"])
def remove_advisor_from_organization(
    organization_id: str, db: Session = Depends(db_session)
) -> bool:
    """
    Remove an advisor from an organization

    Parameters:
        organization_id: ID of the organization to remove the advisor from
        db: Database session

    Returns:
        bool: True if removal was successful, False otherwise
    """
    return OrganizationService(db).remove_advisor_from_organization(organization_id)
