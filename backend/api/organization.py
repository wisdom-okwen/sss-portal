from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.services.organization import OrganizationService
from backend.models.organization import Organization
from backend.database import db_session

api = APIRouter(prefix="/api/organization")
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


@api.get(
    "/by_slug/{slug}", 
    response_model=Organization, 
    responses={404: {"description": "Organization with slug not found"}},
    tags=["Organizations"]
)
def get_organization_by_slug(
    slug: str, db: Session = Depends(db_session)
) -> Organization:
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
def get_organization_by_id(
    organization_id: int, db: Session = Depends(db_session)
) -> Organization:
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
    organization_id: int, organization: Organization, db: Session = Depends(db_session)
) -> Organization:
    """
    Update an existing organization

    Parameters:
        organization_id: ID of the organization to update
        organization: The updated organization data
        db: Database session

    Returns:
        Organization: The updated `Organization`, or None if not found
    """
    return OrganizationService(db).update_organization(organization_id, organization)


@api.delete("/{organization_id}", response_model=Organization, tags=["Organizations"])
def delete_organization(
    organization_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Delete an organization by ID

    Parameters:
        organization_id: ID of the organization to delete
        db: Database session

    Returns:
        Organization: The deleted `Organization`, or None if not found
    """
    return OrganizationService(db).delete_organization(organization_id)


@api.get("/user/{user_id}", response_model=list[Organization], tags=["Organizations"])
def get_organizations_by_user(
    user_id: int, db: Session = Depends(db_session)
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
def get_organization_members(
    organization_id: int, db: Session = Depends(db_session)
) -> list[User]:
    """
    Get members of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve members for
        db: Database session

    Returns:
        list[User]: List of `User`s who are members of the organization
    """
    return OrganizationService(db).get_organization_members(organization_id)


@api.post(
    "/{organization_id}/members", response_model=Organization, tags=["Organizations"]
)
def add_member_to_organization(
    organization_id: int, user_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Add a member to an organization

    Parameters:
        organization_id: ID of the organization to add the member to
        user_id: The user ID to add as a member
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new member added
    """
    return OrganizationService(db).add_member_to_organization(organization_id, user_id)


@api.delete(
    "/{organization_id}/members/{user_id}", response_model=bool, tags=["Organizations"]
)
def remove_member_from_organization(
    organization_id: int, user_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Remove a member from an organization

    Parameters:
        organization_id: ID of the organization to remove the member from
        user_id: ID of the user to remove
        db: Database session

    Returns:
        Organization: The updated `Organization`
    """
    return OrganizationService(db).remove_member_from_organization(
        organization_id, user_id
    )


@api.get(
    "/{organization_id}/admins",
    response_model=list[User],
    tags=["Organizations"],
)
def get_org_admins(
    organization_id: int, db: Session = Depends(db_session)
) -> list[User]:
    """
    Get admin members of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve admins for
        db: Database session

    Returns:
        list[User]: List of `User`s who are admins in the organization
    """
    return OrganizationService(db).get_org_admins(organization_id)


@api.post(
    "/{organization_id}/admins", response_model=Organization, tags=["Organizations"]
)
def add_admin_to_organization(
    organization_id: int, user_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Add an admin to an organization

    Parameters:
        organization_id: ID of the organization to add the admin to
        user_id: The user ID to add as an admin
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new admin added
    """
    return OrganizationService(db).add_admin_to_organization(organization_id, user_id)

@api.delete(
    "/{organization_id}/admins/{user_id}", response_model=bool, tags=["Organizations"]
)
def remove_admin_from_organization(
    organization_id: int, user_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Remove an admin from an organization

    Parameters:
        organization_id: ID of the organization to remove the admin from
        user_id: ID of the user to remove
        db: Database session

    Returns:
        Organization: The updated `Organization`
    """
    return OrganizationService(db).remove_admin_from_organization(
        organization_id, user_id
    )

@api.get(
    "/{organization_id}/teachers",
    response_model=list[User],
    tags=["Organizations"],
)
def get_org_teachers(
    organization_id: int, db: Session = Depends(db_session)
) -> list[User]:
    """
    Get teachers of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve teachers for
        db: Database session

    Returns:
        list[User]: List of `User`s who are teachers in the organization
    """
    return OrganizationService(db).get_org_teachers(organization_id)

@api.post(
    "/{organization_id}/teachers", response_model=Organization, tags=["Organizations"]
)
def add_teacher_to_organization(
    organization_id: int, user_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Add a teacher to an organization

    Parameters:
        organization_id: ID of the organization to add the teacher to
        user_id: The user ID to add as a teacher
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new teacher added
    """
    return OrganizationService(db).add_teacher_to_organization(organization_id, user_id)


@api.get(
    "/{organization_id}/advisor", response_model=User, tags=["Organizations"]
)
def get_organization_advisor(
    organization_id: int, db: Session = Depends(db_session)
) -> User | None:
    """
    Get the advisor of a specific organization

    Parameters:
        organization_id: ID of the organization to retrieve the advisor for
        db: Database session

    Returns:
        User | None: The `User` who is the advisor, or None if not found
    """
    return OrganizationService(db).get_organization_advisor(organization_id)


@api.post(
    "/{organization_id}/advisor", response_model=Organization, tags=["Organizations"]
)
def set_advisor_for_organization(
    organization_id: int, user_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Add an advisor to an organization

    Parameters:
        organization_id: ID of the organization to add the advisor to
        user_id: The user ID to add as an advisor
        db: Database session

    Returns:
        Organization: The updated `Organization` with the new advisor added
    """
    return OrganizationService(db).set_advisor_for_organization(organization_id, user_id)


@api.delete("/{organization_id}/advisor", response_model=bool, tags=["Organizations"])
def remove_advisor_from_organization(
    organization_id: int, db: Session = Depends(db_session)
) -> Organization:
    """
    Remove an advisor from an organization

    Parameters:
        organization_id: ID of the organization to remove the advisor from
        db: Database session

    Returns:
        Organization: The updated `Organization` without the advisor
    """
    return OrganizationService(db).remove_advisor_from_organization(organization_id)
