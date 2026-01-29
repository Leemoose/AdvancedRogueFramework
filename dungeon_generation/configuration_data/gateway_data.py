"""
Gateway Data Module
===================

Configuration for branch connections via gateways.
Defines which branches connect to which, at what depths, and whether connections
are one-way or two-way.

Gateway Types:
    - Hub gateways: One-way connections FROM Hub TO other branches
    - Return gateways: One-way connections from final floor of branch back TO Hub
    - Random gateways: Configurable connections between any branches (can be two-way)

Connection Model:
    - Hub has one-way gateways TO each branch (player chooses which branch to enter)
    - Last floor of each branch has a one-way gateway back to Hub
    - Additional branch-to-branch connections are configurable and can appear randomly
"""

from collections import namedtuple
from typing import List, Dict, Optional, Tuple


# Represents a specific location in the dungeon (branch + depth)
Lair = namedtuple("Lair", ["branch", "depth"])


class GatewayConnection:
    """
    Represents a connection between two lairs (branch/depth combinations).

    Attributes:
        source: The source Lair (where the gateway is located)
        destination: The destination Lair (where the gateway leads)
        two_way: If True, creates gateways in both directions
        random_placement: If True, gateway is placed randomly; if False, placed in dedicated room
        spawn_chance: Probability (0.0-1.0) that this gateway spawns (for random connections)
    """
    def __init__(self, source: Lair, destination: Lair, two_way: bool = False,
                 random_placement: bool = True, spawn_chance: float = 1.0):
        self.source = source
        self.destination = destination
        self.two_way = two_way
        self.random_placement = random_placement
        self.spawn_chance = spawn_chance

    def __repr__(self):
        direction = "<->" if self.two_way else "->"
        return f"GatewayConnection({self.source} {direction} {self.destination})"


class GatewayData:
    """
    Configuration data for all gateway connections between branches.

    The gateway system supports:
        - Hub-centric connections (Hub -> branches, branch final floors -> Hub)
        - Direct branch-to-branch connections
        - One-way and two-way connections
        - Random placement with configurable spawn chances

    Developers can modify the connections list to customize branch topology.
    """

    def __init__(self):
        # Master list of all gateway connections
        # Modify this list to change branch connectivity
        self.connections: List[GatewayConnection] = []

        # Cache for quick lookup: maps Lair -> list of destination Lairs
        self._gateway_map: Dict[Lair, List[Lair]] = {}

        # Cache for connection details
        self._connection_details: Dict[Tuple[Lair, Lair], GatewayConnection] = {}

        # Define default connections
        self._setup_default_connections()

        # Build lookup caches
        self._build_cache()

    def _setup_default_connections(self):
        """
        Set up the default branch connection topology.

        Default topology:
            - Player starts in Dungeon floor 1
            - Dungeon floor 10 -> Hub (one-way, player reaches Hub after completing Dungeon)
            - Hub -> all branches (one-way, Hub is the central nexus)
            - Each branch's final floor -> Hub (one-way, return to Hub after completing branch)
            - Optional random connections between branches (configurable)
        """

        # =====================================================================
        # HUB CONNECTIONS (one-way outbound from Hub)
        # =====================================================================
        # Hub connects to the first floor of each branch
        # Players use Hub to choose which branch to explore

        self.connections.extend([
            # Hub -> Dungeon floor 1 (allows return to Dungeon from Hub)
            GatewayConnection(
                source=Lair("Hub", 1),
                destination=Lair("Dungeon", 1),
                two_way=False,
                random_placement=False  # Dedicated placement in Hub
            ),
            # Hub -> Forest floor 1
            GatewayConnection(
                source=Lair("Hub", 1),
                destination=Lair("Forest", 1),
                two_way=False,
                random_placement=False
            ),
            # Hub -> Ocean floor 1
            GatewayConnection(
                source=Lair("Hub", 1),
                destination=Lair("Ocean", 1),
                two_way=False,
                random_placement=False
            ),
            # Hub -> Throne floor 1
            GatewayConnection(
                source=Lair("Hub", 1),
                destination=Lair("Throne", 1),
                two_way=False,
                random_placement=False
            ),
        ])

        # =====================================================================
        # RETURN CONNECTIONS (one-way from branch final floors back to Hub)
        # =====================================================================
        # Final floor of each branch has a gateway back to Hub

        self.connections.extend([
            # Dungeon floor 10 -> Hub (this is how player first reaches Hub)
            GatewayConnection(
                source=Lair("Dungeon", 10),
                destination=Lair("Hub", 1),
                two_way=False,
                random_placement=False  # Always present on final floor
            ),
            # Forest floor 5 -> Hub
            GatewayConnection(
                source=Lair("Forest", 5),
                destination=Lair("Hub", 1),
                two_way=False,
                random_placement=False
            ),
            # Ocean floor 1 -> Hub (Ocean is only 1 floor)
            GatewayConnection(
                source=Lair("Ocean", 1),
                destination=Lair("Hub", 1),
                two_way=False,
                random_placement=False
            ),
            # Throne floor 1 -> Hub (Throne is only 1 floor)
            GatewayConnection(
                source=Lair("Throne", 1),
                destination=Lair("Hub", 1),
                two_way=False,
                random_placement=False
            ),
        ])

        # =====================================================================
        # RANDOM BRANCH-TO-BRANCH CONNECTIONS (optional, configurable)
        # =====================================================================
        # These connections can appear randomly on various floors
        # Developers can add/remove/modify these as desired

        # Example: Forest and Dungeon mid-level connection
        # self.connections.append(
        #     GatewayConnection(
        #         source=Lair("Dungeon", 5),
        #         destination=Lair("Forest", 3),
        #         two_way=True,  # Can travel both directions
        #         random_placement=True,
        #         spawn_chance=0.5  # 50% chance to appear
        #     )
        # )

    def _build_cache(self):
        """Build lookup caches from the connections list."""
        self._gateway_map.clear()
        self._connection_details.clear()

        for conn in self.connections:
            # Add source -> destination mapping
            if conn.source not in self._gateway_map:
                self._gateway_map[conn.source] = []
            self._gateway_map[conn.source].append(conn.destination)
            self._connection_details[(conn.source, conn.destination)] = conn

            # If two-way, also add reverse mapping
            if conn.two_way:
                if conn.destination not in self._gateway_map:
                    self._gateway_map[conn.destination] = []
                self._gateway_map[conn.destination].append(conn.source)
                # Create reverse connection details
                reverse_conn = GatewayConnection(
                    source=conn.destination,
                    destination=conn.source,
                    two_way=True,
                    random_placement=conn.random_placement,
                    spawn_chance=conn.spawn_chance
                )
                self._connection_details[(conn.destination, conn.source)] = reverse_conn

    def has_gateway(self, branch: str, depth: int) -> bool:
        """
        Check if a branch/depth has any gateway connections.

        Args:
            branch: The branch name
            depth: The floor depth

        Returns:
            True if there are gateways at this location
        """
        lair = Lair(branch, depth)
        return lair in self._gateway_map and len(self._gateway_map[lair]) > 0

    def get_num_gateways(self, branch: str, depth: int) -> int:
        """
        Get the number of gateways at a branch/depth.

        Args:
            branch: The branch name
            depth: The floor depth

        Returns:
            Number of gateway connections at this location
        """
        lair = Lair(branch, depth)
        if lair not in self._gateway_map:
            return 0
        return len(self._gateway_map[lair])

    def get_destinations(self, branch: str, depth: int) -> List[Lair]:
        """
        Get all destination lairs for gateways at a branch/depth.

        Args:
            branch: The branch name
            depth: The floor depth

        Returns:
            List of destination Lair objects
        """
        lair = Lair(branch, depth)
        return self._gateway_map.get(lair, [])

    def get_connection(self, source_branch: str, source_depth: int,
                       dest_branch: str, dest_depth: int) -> Optional[GatewayConnection]:
        """
        Get the connection details between two specific lairs.

        Args:
            source_branch: Source branch name
            source_depth: Source floor depth
            dest_branch: Destination branch name
            dest_depth: Destination floor depth

        Returns:
            GatewayConnection object if connection exists, None otherwise
        """
        source = Lair(source_branch, source_depth)
        dest = Lair(dest_branch, dest_depth)
        return self._connection_details.get((source, dest))

    def is_random_placement(self, branch: str, depth: int) -> bool:
        """
        Check if gateways at this location should be randomly placed.

        Args:
            branch: The branch name
            depth: The floor depth

        Returns:
            True if any gateway at this location uses random placement
        """
        lair = Lair(branch, depth)
        if lair not in self._gateway_map:
            return False

        for dest in self._gateway_map[lair]:
            conn = self._connection_details.get((lair, dest))
            if conn and conn.random_placement:
                return True
        return False

    def get_spawn_chance(self, source_branch: str, source_depth: int,
                         dest_branch: str, dest_depth: int) -> float:
        """
        Get the spawn chance for a specific gateway connection.

        Args:
            source_branch: Source branch name
            source_depth: Source floor depth
            dest_branch: Destination branch name
            dest_depth: Destination floor depth

        Returns:
            Spawn chance (0.0-1.0), or 1.0 if connection not found
        """
        conn = self.get_connection(source_branch, source_depth, dest_branch, dest_depth)
        return conn.spawn_chance if conn else 1.0

    def add_connection(self, source_branch: str, source_depth: int,
                       dest_branch: str, dest_depth: int,
                       two_way: bool = False, random_placement: bool = True,
                       spawn_chance: float = 1.0):
        """
        Add a new gateway connection (for runtime configuration).

        Args:
            source_branch: Source branch name
            source_depth: Source floor depth
            dest_branch: Destination branch name
            dest_depth: Destination floor depth
            two_way: If True, creates bidirectional connection
            random_placement: If True, gateway placed randomly
            spawn_chance: Probability of gateway appearing
        """
        conn = GatewayConnection(
            source=Lair(source_branch, source_depth),
            destination=Lair(dest_branch, dest_depth),
            two_way=two_way,
            random_placement=random_placement,
            spawn_chance=spawn_chance
        )
        self.connections.append(conn)
        self._build_cache()

    def remove_connection(self, source_branch: str, source_depth: int,
                          dest_branch: str, dest_depth: int):
        """
        Remove a gateway connection.

        Args:
            source_branch: Source branch name
            source_depth: Source floor depth
            dest_branch: Destination branch name
            dest_depth: Destination floor depth
        """
        source = Lair(source_branch, source_depth)
        dest = Lair(dest_branch, dest_depth)

        self.connections = [
            c for c in self.connections
            if not (c.source == source and c.destination == dest)
        ]
        self._build_cache()

    def get_all_gateway_lairs(self) -> List[Lair]:
        """
        Get all lairs that have gateway connections.

        Returns:
            List of all Lair objects that have gateways
        """
        return list(self._gateway_map.keys())
