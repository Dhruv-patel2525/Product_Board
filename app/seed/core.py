from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.core.db import async_session


# ---------- Seed data ----------

PERMISSIONS_SEED = [
    {"code": "org.view", "description": "View organization details"},
    {"code": "org.manage_settings", "description": "Update organization settings"},
    {"code": "org.manage_members", "description": "Invite, remove, and change roles of members"},
    {"code": "org.manage_billing", "description": "View and manage billing and subscription"},

    {"code": "product.view", "description": "View products and product boards"},
    {"code": "product.create", "description": "Create new products"},
    {"code": "product.edit", "description": "Edit existing products"},
    {"code": "product.archive", "description": "Archive or unarchive products"},
    {"code": "product.delete", "description": "Permanently delete products"},

    {"code": "feedback.view", "description": "View feedback items"},
    {"code": "feedback.create", "description": "Create new feedback items"},
    {"code": "feedback.edit_own", "description": "Edit own feedback"},
    {"code": "feedback.edit_all", "description": "Edit all feedback"},
    {"code": "feedback.delete_own", "description": "Delete own feedback"},
    {"code": "feedback.delete_all", "description": "Delete any feedback"},
    {"code": "feedback.change_status", "description": "Change feedback status"},

    {"code": "comment.view", "description": "View comments"},
    {"code": "comment.create", "description": "Add comments"},
    {"code": "comment.edit_own", "description": "Edit own comments"},
    {"code": "comment.delete_own", "description": "Delete own comments"},
    {"code": "comment.moderate", "description": "Moderate any comment"},

    {"code": "vote.create", "description": "Add votes to feedback"},
    {"code": "vote.revoke", "description": "Remove own votes"},
    {"code": "vote.view_counts", "description": "View vote counts and analytics"},

    {"code": "roadmap.view", "description": "View roadmap"},
    {"code": "roadmap.edit", "description": "Edit roadmap"},

    {"code": "tag.manage", "description": "Create and manage tags/categories"},
    {"code": "segment.manage", "description": "Manage customer segments and filters"},

    {"code": "system.admin", "description": "Full system administrative access"},
]

ROLES_SEED = [
    {"key": "OWNER", "description": "Org owner with full access", "is_system": True, "org_id": None},
    {"key": "ADMIN", "description": "Org admin with broad access", "is_system": True, "org_id": None},
    {"key": "PRODUCT_MANAGER", "description": "Manages products, feedback, roadmap", "is_system": True, "org_id": None},
    {"key": "CONTRIBUTOR", "description": "Can add feedback, comment, and collaborate", "is_system": True, "org_id": None},
    {"key": "VIEWER", "description": "Read-only member with limited interaction", "is_system": True, "org_id": None},
]

ROLE_PERMISSIONS_MAP = {
    "OWNER": [
        "org.view", "org.manage_settings", "org.manage_members", "org.manage_billing",
        "product.view", "product.create", "product.edit", "product.archive", "product.delete",
        "feedback.view", "feedback.create", "feedback.edit_own", "feedback.edit_all",
        "feedback.delete_own", "feedback.delete_all", "feedback.change_status",
        "comment.view", "comment.create", "comment.edit_own", "comment.delete_own", "comment.moderate",
        "vote.create", "vote.revoke", "vote.view_counts",
        "roadmap.view", "roadmap.edit",
        "tag.manage", "segment.manage",
        "system.admin",
    ],
    "ADMIN": [
        "org.view", "org.manage_settings", "org.manage_members",
        "product.view", "product.create", "product.edit", "product.archive",
        "feedback.view", "feedback.create", "feedback.edit_own", "feedback.edit_all",
        "feedback.delete_own", "feedback.delete_all", "feedback.change_status",
        "comment.view", "comment.create", "comment.edit_own", "comment.delete_own", "comment.moderate",
        "vote.create", "vote.revoke", "vote.view_counts",
        "roadmap.view", "roadmap.edit",
        "tag.manage", "segment.manage",
    ],
    "PRODUCT_MANAGER": [
        "org.view",
        "product.view", "product.create", "product.edit", "product.archive",
        "feedback.view", "feedback.create", "feedback.edit_own", "feedback.edit_all",
        "feedback.delete_own", "feedback.change_status",
        "comment.view", "comment.create", "comment.edit_own", "comment.delete_own",
        "vote.create", "vote.revoke", "vote.view_counts",
        "roadmap.view", "roadmap.edit",
        "tag.manage", "segment.manage",
    ],
    "CONTRIBUTOR": [
        "org.view",
        "product.view",
        "feedback.view", "feedback.create", "feedback.edit_own", "feedback.delete_own",
        "comment.view", "comment.create", "comment.edit_own", "comment.delete_own",
        "vote.create", "vote.revoke", "vote.view_counts",
        "roadmap.view",
    ],
    "VIEWER": [
        "org.view",
        "product.view",
        "feedback.view",
        "comment.view",
        "vote.create",
        "vote.view_counts",
        "roadmap.view",
    ],
}


# ---------- Async seed functions ----------

async def seed_permissions(session: AsyncSession) -> None:
    for p in PERMISSIONS_SEED:
        stmt = select(Permission).where(Permission.code == p["code"])
        result = await session.exec(stmt)
        existing = result.one_or_none()
        if existing:
            if existing.description != p["description"]:
                existing.description = p["description"]
        else:
            session.add(Permission(code=p["code"], description=p["description"]))


async def seed_roles(session: AsyncSession) -> None:
    for r in ROLES_SEED:
        stmt = select(Role).where(
            Role.key == r["key"],
            Role.org_id == r["org_id"],
        )
        result = await session.exec(stmt)
        existing = result.one_or_none()
        if existing:
            if existing.description != r["description"]:
                existing.description = r["description"]
            if existing.is_system != r["is_system"]:
                existing.is_system = r["is_system"]
        else:
            session.add(
                Role(
                    key=r["key"],
                    description=r["description"],
                    is_system=r["is_system"],
                    org_id=r["org_id"],
                )
            )


async def seed_role_permissions(session: AsyncSession) -> None:
    perms_result = await session.exec(select(Permission))
    perms = {p.code: p for p in perms_result.all()}

    roles_result = await session.exec(
        select(Role).where(Role.org_id == None)  # system roles only
    )
    roles = {r.key: r for r in roles_result.all()}

    for role_key, perm_codes in ROLE_PERMISSIONS_MAP.items():
        role = roles.get(role_key)
        if not role:
            continue

        for code in perm_codes:
            perm = perms.get(code)
            if not perm:
                continue

            stmt = select(RolePermission).where(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == perm.id,
            )
            result = await session.exec(stmt)
            existing = result.one_or_none()
            if not existing:
                session.add(
                    RolePermission(role_id=role.id, permission_id=perm.id)
                )


async def seed_core() -> None:
    async with async_session() as session:
        await seed_permissions(session)
        await seed_roles(session)
        await session.commit()

        await seed_role_permissions(session)
        await session.commit()
