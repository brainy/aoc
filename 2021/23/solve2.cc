#include <algorithm>
#include <array>
#include <cstdio>               // std::format is not widely supported yet
#include <cstdint>
#include <functional>
#include <memory>
#include <numeric>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;

struct amphipod;
struct puzzle
{
    struct node;
    struct path
    {
        const node* next {nullptr};
        uint64_t cost {0};
        operator bool() const noexcept { return !!next; }
    };

    struct node
    {
        const bool room;
        const char type;
        path left;
        path right;
        path lroom;
        path rroom;
        path down;
        path up;

        unordered_set<const amphipod*> ltarget {};
        unordered_set<const amphipod*> rtarget {};
    };

    node hallway_01 {false, '\0'};
    node hallway_02 {false, '\0'};
    // Rule 1: node hallway_03 is unreachable
    node hallway_04 {false, '\0'};
    // Rule 1: node hallway_05 is unreachable
    node hallway_06 {false, '\0'};
    // Rule 1: node hallway_07 is unreachable
    node hallway_08 {false, '\0'};
    // Rule 1: node hallway_09 is unreachable
    node hallway_10 {false, '\0'};
    node hallway_11 {false, '\0'};
    node room_A_1 {true, 'A'};
    node room_A_2 {true, 'A'};
    node room_A_3 {true, 'A'};
    node room_A_4 {true, 'A'};
    node room_B_1 {true, 'B'};
    node room_B_2 {true, 'B'};
    node room_B_3 {true, 'B'};
    node room_B_4 {true, 'B'};
    node room_C_1 {true, 'C'};
    node room_C_2 {true, 'C'};
    node room_C_3 {true, 'C'};
    node room_C_4 {true, 'C'};
    node room_D_1 {true, 'D'};
    node room_D_2 {true, 'D'};
    node room_D_3 {true, 'D'};
    node room_D_4 {true, 'D'};

    puzzle();
};

const puzzle PUZZLE;

struct amphipod
{
    char type;
    uint64_t cost;
    array<const puzzle::node*, 4> rooms;
    bool owns(const puzzle::node* node) const noexcept
      {
          return type == node->type;
      }
};

const amphipod POD_A {'A',    1, {&PUZZLE.room_A_4, &PUZZLE.room_A_3, &PUZZLE.room_A_2, &PUZZLE.room_A_1}};
const amphipod POD_B {'B',   10, {&PUZZLE.room_B_4, &PUZZLE.room_B_3, &PUZZLE.room_B_2, &PUZZLE.room_B_1}};
const amphipod POD_C {'C',  100, {&PUZZLE.room_C_4, &PUZZLE.room_C_3, &PUZZLE.room_C_2, &PUZZLE.room_C_1}};
const amphipod POD_D {'D', 1000, {&PUZZLE.room_D_4, &PUZZLE.room_D_3, &PUZZLE.room_D_2, &PUZZLE.room_D_1}};

puzzle::puzzle()
{
    hallway_01.right = path{&hallway_02, 1};
    hallway_01.rtarget.insert(&POD_A);
    hallway_01.rtarget.insert(&POD_B);
    hallway_01.rtarget.insert(&POD_C);
    hallway_01.rtarget.insert(&POD_D);

    hallway_02.left = path{&hallway_01, 1};
    hallway_02.right = path{&hallway_04, 2};
    hallway_02.rroom = path{&room_A_4, 2};
    hallway_02.rtarget.insert(&POD_A);
    hallway_02.rtarget.insert(&POD_B);
    hallway_02.rtarget.insert(&POD_C);
    hallway_02.rtarget.insert(&POD_D);

    hallway_04.left = path{&hallway_02, 2};
    hallway_04.right = path{&hallway_06, 2};
    hallway_04.lroom = path{&room_A_4, 2};
    hallway_04.rroom = path{&room_B_4, 2};
    hallway_04.ltarget.insert(&POD_A);
    hallway_04.rtarget.insert(&POD_B);
    hallway_04.rtarget.insert(&POD_C);
    hallway_04.rtarget.insert(&POD_D);

    hallway_06.left = path{&hallway_04, 2};
    hallway_06.right = path{&hallway_08, 2};
    hallway_06.lroom = path{&room_B_4, 2};
    hallway_06.rroom = path{&room_C_4, 2};
    hallway_06.ltarget.insert(&POD_A);
    hallway_06.ltarget.insert(&POD_B);
    hallway_06.rtarget.insert(&POD_C);
    hallway_06.rtarget.insert(&POD_D);

    hallway_08.left = path{&hallway_06, 2};
    hallway_08.right = path{&hallway_10, 2};
    hallway_08.lroom = path{&room_C_4, 2};
    hallway_08.rroom = path{&room_D_4, 2};
    hallway_08.ltarget.insert(&POD_A);
    hallway_08.ltarget.insert(&POD_B);
    hallway_08.ltarget.insert(&POD_C);
    hallway_08.rtarget.insert(&POD_D);

    hallway_10.left = path{&hallway_08, 2};
    hallway_10.right = path{&hallway_11, 1};
    hallway_10.lroom = path{&room_D_4, 2};
    hallway_10.ltarget.insert(&POD_A);
    hallway_10.ltarget.insert(&POD_B);
    hallway_10.ltarget.insert(&POD_C);
    hallway_10.ltarget.insert(&POD_D);

    hallway_11.left = path{&hallway_10, 1};
    hallway_11.ltarget.insert(&POD_A);
    hallway_11.ltarget.insert(&POD_B);
    hallway_11.ltarget.insert(&POD_C);
    hallway_11.ltarget.insert(&POD_D);

    room_A_1.up = path{&room_A_2, 1};
    room_A_1.rtarget.insert(&POD_B);
    room_A_1.rtarget.insert(&POD_C);
    room_A_1.rtarget.insert(&POD_D);

    room_A_2.up = path{&room_A_3, 1};
    room_A_2.down = path{&room_A_1, 1};
    room_A_2.rtarget.insert(&POD_B);
    room_A_2.rtarget.insert(&POD_C);
    room_A_2.rtarget.insert(&POD_D);

    room_A_3.up = path{&room_A_4, 1};
    room_A_3.down = path{&room_A_2, 1};
    room_A_3.rtarget.insert(&POD_B);
    room_A_3.rtarget.insert(&POD_C);
    room_A_3.rtarget.insert(&POD_D);

    room_A_4.down = path{&room_A_3, 1};
    room_A_4.left = path{&hallway_02, 2};
    room_A_4.right = path{&hallway_04, 2};
    room_A_4.rtarget.insert(&POD_B);
    room_A_4.rtarget.insert(&POD_C);
    room_A_4.rtarget.insert(&POD_D);

    room_B_1.up = path{&room_B_2, 1};
    room_B_1.ltarget.insert(&POD_A);
    room_B_1.rtarget.insert(&POD_C);
    room_B_1.rtarget.insert(&POD_D);

    room_B_2.up = path{&room_B_3, 1};
    room_B_2.down = path{&room_B_1, 1};
    room_B_2.ltarget.insert(&POD_A);
    room_B_2.rtarget.insert(&POD_C);
    room_B_2.rtarget.insert(&POD_D);

    room_B_3.up = path{&room_B_4, 1};
    room_B_3.down = path{&room_B_2, 1};
    room_B_3.ltarget.insert(&POD_A);
    room_B_3.rtarget.insert(&POD_C);
    room_B_3.rtarget.insert(&POD_D);

    room_B_4.down = path{&room_B_3, 1};
    room_B_4.left = path{&hallway_04, 2};
    room_B_4.right = path{&hallway_06, 2};
    room_B_4.ltarget.insert(&POD_A);
    room_B_4.rtarget.insert(&POD_C);
    room_B_4.rtarget.insert(&POD_D);

    room_C_1.up = path{&room_C_2, 1};
    room_C_1.ltarget.insert(&POD_A);
    room_C_1.ltarget.insert(&POD_B);
    room_C_1.rtarget.insert(&POD_D);

    room_C_2.up = path{&room_C_3, 1};
    room_C_2.down = path{&room_C_1, 1};
    room_C_2.ltarget.insert(&POD_A);
    room_C_2.ltarget.insert(&POD_B);
    room_C_2.rtarget.insert(&POD_D);

    room_C_3.up = path{&room_C_4, 1};
    room_C_3.down = path{&room_C_2, 1};
    room_C_3.ltarget.insert(&POD_A);
    room_C_3.ltarget.insert(&POD_B);
    room_C_3.rtarget.insert(&POD_D);

    room_C_4.down = path{&room_C_3, 1};
    room_C_4.left = path{&hallway_06, 2};
    room_C_4.right = path{&hallway_08, 2};
    room_C_4.ltarget.insert(&POD_A);
    room_C_4.ltarget.insert(&POD_B);
    room_C_4.rtarget.insert(&POD_D);

    room_D_1.up = path{&room_D_2, 1};
    room_D_1.ltarget.insert(&POD_A);
    room_D_1.ltarget.insert(&POD_B);
    room_D_1.ltarget.insert(&POD_C);

    room_D_2.up = path{&room_D_3, 1};
    room_D_2.down = path{&room_D_1, 1};
    room_D_2.ltarget.insert(&POD_A);
    room_D_2.ltarget.insert(&POD_B);
    room_D_2.ltarget.insert(&POD_C);

    room_D_3.up = path{&room_D_4, 1};
    room_D_3.down = path{&room_D_2, 1};
    room_D_3.ltarget.insert(&POD_A);
    room_D_3.ltarget.insert(&POD_B);
    room_D_3.ltarget.insert(&POD_C);

    room_D_4.down = path{&room_D_3, 1};
    room_D_4.left = path{&hallway_08, 2};
    room_D_4.right = path{&hallway_10, 2};
    room_D_4.ltarget.insert(&POD_A);
    room_D_4.ltarget.insert(&POD_B);
    room_D_4.ltarget.insert(&POD_C);
}


struct state
{
    struct position
    {
        const amphipod* pod {nullptr};
        const puzzle::node* node {nullptr};

        bool operator==(const position& other) const noexcept
          {
              return pod == other.pod && node == other.node;
          }
        bool operator<(const position& other) const noexcept
          {
              return (pod->type < other.pod->type
                      || uintptr_t(node) < uintptr_t(other.node));
          }
    };
    using positions = array<position, 16>;

    positions pos;

    bool operator==(const state& other) const noexcept
      {
          return pos == other.pos;
      }

    constexpr state() = default;
    constexpr state(const positions& pos_) : pos{pos_}
      {
          sort(pos.begin(), pos.end());
      }
    constexpr state(positions&& pos_) : pos{std::move(pos_)}
      {
          sort(pos.begin(), pos.end());
      }

    auto occupied() const
      {
          return unordered_map<const puzzle::node*, const amphipod*>{
              {pos[0].node, pos[0].pod},
              {pos[1].node, pos[1].pod},
              {pos[2].node, pos[2].pod},
              {pos[3].node, pos[3].pod},
              {pos[4].node, pos[4].pod},
              {pos[5].node, pos[5].pod},
              {pos[6].node, pos[6].pod},
              {pos[7].node, pos[7].pod},
              {pos[8].node, pos[8].pod},
              {pos[9].node, pos[9].pod},
              {pos[10].node, pos[10].pod},
              {pos[11].node, pos[11].pod},
              {pos[12].node, pos[12].pod},
              {pos[13].node, pos[13].pod},
              {pos[14].node, pos[14].pod},
              {pos[15].node, pos[15].pod},
          };
      }

    using pstate = shared_ptr<const state>;
    using onemove = pair<pstate, uint64_t>;
    auto get_moves() const
      {
          const auto occ = occupied();
          auto moves = vector<onemove>{};
          moves.reserve(pos.size());    // This is just a guess.

          for (size_t i = 0; i < pos.size(); ++i)
          {
              const auto& pod = pos[i].pod;
              const auto& node = pos[i].node;

              // The amphipod will move out of its room if there are other types insidde.
              const auto pure_room = all_of(pod->rooms.cbegin(), pod->rooms.cend(),
                                            [&occ, &pod](const puzzle::node* room) -> bool
                                            {
                                                return !occ.count(room) || occ.at(room) == pod;
                                            });

              // Rule 2: The amphipod can only enter its destination if there's
              // space and there are no other type of amphipods inside.
              const auto room_available = !occ.count(pod->rooms[0]) && pure_room;

              if (node->room)
              {
                  if (room_available)
                  {
                      // Find a path to the destination room if room_available;
                      if (!pod->owns(node))
                      {
                          if (find_destination_path(i, occ, node, pod, &moves))
                              continue;
                      }
                      else
                      {
                          // Maybe the amphipod can move further down in its destination room?
                          auto n = node;
                          uint64_t cost = 0;
                          climb_into_room(n, cost, occ, pod->cost);
                          if (cost > 0)
                          {
                              // Yes, it could move.
                              auto newpos = pos;
                              newpos[i].node = n;
                              moves.emplace_back(make_shared<state>(std::move(newpos)), cost);
                          }
                      }
                  }

                  if (!pod->owns(node) || !pure_room)
                  {
                      // Try all reachable positions in the hallway.
                      find_hallway_moves(i, occ, node, pod, &moves);
                  }
              }
              else
              {
                  // Rule 3: Only move from the hallway when there's space
                  // available in the amphipod's destination room.
                  if (!room_available)
                      continue;

                  // Find a path to the amphipod's destination room.
                  find_destination_path(i, occ, node, pod, &moves);
              }
          }

          return moves;
      }

    bool find_destination_path(const size_t i,
                               const unordered_map<const puzzle::node*, const amphipod*>& occ,
                               const puzzle::node* node, const amphipod* pod,
                               vector<onemove>* moves) const
      {
          if (node->ltarget.count(pod))
              return find_destination_path_left(i, occ, node, pod, moves);
          else if (node->rtarget.count(pod))
              return find_destination_path_right(i, occ, node, pod, moves);
          else
              assert(!"Broken layout, no destination either right or left.");
          return false;
      }

    bool find_destination_path_left(const size_t i,
                                    const unordered_map<const puzzle::node*, const amphipod*>& occ,
                                    const puzzle::node* node, const amphipod* pod,
                                    vector<onemove>* moves) const
      {
          uint64_t cost = 0;
          if (!climb_out_of_room(node, cost, occ, pod->cost))
              return false;

          assert(!node->up);
          while (node->left)
          {
              if (node->lroom && pod->owns(node->lroom.next))
              {
                  assert(node->lroom.next == pod->rooms[0]);
                  assert(!occ.count(pod->rooms[0]));
                  cost += node->lroom.cost * pod->cost;
                  node = node->lroom.next;
                  climb_into_room(node, cost, occ, pod->cost);
                  assert(!node->down || occ.at(node->down.next) == pod);
                  auto newpos = pos;
                  newpos[i].node = node;
                  moves->emplace_back(make_shared<state>(std::move(newpos)), cost);
                  return true;
              }
              cost += node->left.cost * pod->cost;
              node = node->left.next;
              if (occ.count(node))
                  break;
          }

          return false;
      }

    bool find_destination_path_right(const size_t i,
                                     const unordered_map<const puzzle::node*, const amphipod*>& occ,
                                     const puzzle::node* node, const amphipod* pod,
                                     vector<onemove>* moves) const
      {
          uint64_t cost = 0;
          if (!climb_out_of_room(node, cost, occ, pod->cost))
              return false;

          assert(!node->up);
          while (node->right)
          {
              if (node->rroom && pod->owns(node->rroom.next))
              {
                  assert(node->rroom.next == pod->rooms[0]);
                  assert(!occ.count(pod->rooms[0]));
                  cost += node->rroom.cost * pod->cost;
                  node = node->rroom.next;
                  climb_into_room(node, cost, occ, pod->cost);
                  assert(!node->down || occ.at(node->down.next) == pod);
                  auto newpos = pos;
                  newpos[i].node = node;
                  moves->emplace_back(make_shared<state>(std::move(newpos)), cost);
                  return true;
              }
              cost += node->right.cost * pod->cost;
              node = node->right.next;
              if (occ.count(node))
                  break;
          }

          return false;
      }

    bool find_hallway_moves(const size_t i,
                            const unordered_map<const puzzle::node*, const amphipod*>& occ,
                            const puzzle::node* node, const amphipod* pod,
                            vector<onemove>* moves) const
      {
          uint64_t cost = 0;
          if (!climb_out_of_room(node, cost, occ, pod->cost))
              return false;

          assert(!node->up);
          if (!node->left && !node->right)
              return false;

          auto newpos = pos;
          const auto ctart = cost;
          const auto start = node;

          // Move left as far as possible.
          while (node->left && !occ.count(node->left.next))
          {
              cost += node->left.cost * pod->cost;
              newpos[i].node = node->left.next;
              node = node->left.next;
              moves->emplace_back(make_shared<state>(newpos), cost);
          }

          // Move right as far as possible.
          cost = ctart;
          node = start;
          while (node->right && !occ.count(node->right.next))
          {
              cost += node->right.cost * pod->cost;
              newpos[i].node = node->right.next;
              node = node->right.next;
              moves->emplace_back(make_shared<state>(newpos), cost);
          }

          return true;
      }

    bool climb_out_of_room(const puzzle::node*& node, uint64_t& moved_cost,
                           const unordered_map<const puzzle::node*, const amphipod*>& occ,
                           uint64_t pod_cost) const
      {
          if (!node->room)
              return true;

          uint64_t cost = 0;
          const puzzle::node* n = node;
          while(n->up)
          {
              if (occ.count(n->up.next))
              {
                  // Don't move until there's space to move into a hallway.
                  return false;
              }
              cost += n->up.cost * pod_cost;
              n = n->up.next;
          }
          moved_cost += cost;
          node = n;
          return true;
      }

    void climb_into_room(const puzzle::node*& node, uint64_t& moved_cost,
                         const unordered_map<const puzzle::node*, const amphipod*>& occ,
                         uint64_t pod_cost) const
      {
          assert(node->room);

          uint64_t cost = 0;
          const puzzle::node* n = node;
          while (n->down)
          {
              if (occ.count(n->down.next))
                  break;
              cost += n->down.cost * pod_cost;
              n = n->down.next;
          }
          moved_cost += cost;
          node = n;
      }

    void display() const
      {
          static const char blue[] = "\x1b[1m\x1b[34m";
          static const char red[] = "\x1b[1m\x1b[31m";
          static const char off[] = "\x1b[0m";
          // Alternative if your terminal doesn't understand ANSI escape codes:
          // static const char blue[] = "";
          // static const char red[] = "";
          // static const char off[] = "";

          static const char layout[] = (
              "#########################\n"
              "# %s%c%s %s%c%s . %s%c%s . %s%c%s . %s%c%s . %s%c%s %s%c%s #\n"
              "##### %s%c%s # %s%c%s # %s%c%s # %s%c%s #####\n"
              "    # %s%c%s # %s%c%s # %s%c%s # %s%c%s #\n"
              "    # %s%c%s # %s%c%s # %s%c%s # %s%c%s #\n"
              "    # %s%c%s # %s%c%s # %s%c%s # %s%c%s #\n"
              "    #################\n");

          const auto occ = occupied();
          printf(layout,
                 !occ.count(&PUZZLE.hallway_01) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_01) ? '.': occ.at(&PUZZLE.hallway_01)->type,
                 !occ.count(&PUZZLE.hallway_01) ? "" : off,

                 !occ.count(&PUZZLE.hallway_02) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_02) ? '.': occ.at(&PUZZLE.hallway_02)->type,
                 !occ.count(&PUZZLE.hallway_02) ? "" : off,

                 !occ.count(&PUZZLE.hallway_04) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_04) ? '.': occ.at(&PUZZLE.hallway_04)->type,
                 !occ.count(&PUZZLE.hallway_04) ? "" : off,

                 !occ.count(&PUZZLE.hallway_06) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_06) ? '.': occ.at(&PUZZLE.hallway_06)->type,
                 !occ.count(&PUZZLE.hallway_06) ? "" : off,

                 !occ.count(&PUZZLE.hallway_08) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_08) ? '.': occ.at(&PUZZLE.hallway_08)->type,
                 !occ.count(&PUZZLE.hallway_08) ? "" : off,

                 !occ.count(&PUZZLE.hallway_10) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_10) ? '.': occ.at(&PUZZLE.hallway_10)->type,
                 !occ.count(&PUZZLE.hallway_10) ? "" : off,

                 !occ.count(&PUZZLE.hallway_11) ? "" : blue,
                 !occ.count(&PUZZLE.hallway_11) ? '.': occ.at(&PUZZLE.hallway_11)->type,
                 !occ.count(&PUZZLE.hallway_11) ? "" : off,

                 !occ.count(&PUZZLE.room_A_4)   ? "" : (
                     occ.at(&PUZZLE.room_A_4)->owns(&PUZZLE.room_A_4) ? red : blue),
                 !occ.count(&PUZZLE.room_A_4)   ? '.': occ.at(&PUZZLE.room_A_4)->type,
                 !occ.count(&PUZZLE.room_A_4)   ? "" : off,

                 !occ.count(&PUZZLE.room_B_4)   ? "" : (
                     occ.at(&PUZZLE.room_B_4)->owns(&PUZZLE.room_B_4) ? red : blue),
                 !occ.count(&PUZZLE.room_B_4)   ? '.': occ.at(&PUZZLE.room_B_4)->type,
                 !occ.count(&PUZZLE.room_B_4)   ? "" : off,

                 !occ.count(&PUZZLE.room_C_4)   ? "" : (
                     occ.at(&PUZZLE.room_C_4)->owns(&PUZZLE.room_C_4) ? red : blue),
                 !occ.count(&PUZZLE.room_C_4)   ? '.': occ.at(&PUZZLE.room_C_4)->type,
                 !occ.count(&PUZZLE.room_C_4)   ? "" : off,

                 !occ.count(&PUZZLE.room_D_4)   ? "" : (
                     occ.at(&PUZZLE.room_D_4)->owns(&PUZZLE.room_D_4) ? red : blue),
                 !occ.count(&PUZZLE.room_D_4)   ? '.': occ.at(&PUZZLE.room_D_4)->type,
                 !occ.count(&PUZZLE.room_D_4)   ? "" : off,

                 !occ.count(&PUZZLE.room_A_3)   ? "" : (
                     occ.at(&PUZZLE.room_A_3)->owns(&PUZZLE.room_A_3) ? red : blue),
                 !occ.count(&PUZZLE.room_A_3)   ? '.': occ.at(&PUZZLE.room_A_3)->type,
                 !occ.count(&PUZZLE.room_A_3)   ? "" : off,

                 !occ.count(&PUZZLE.room_B_3)   ? "" : (
                     occ.at(&PUZZLE.room_B_3)->owns(&PUZZLE.room_B_3) ? red : blue),
                 !occ.count(&PUZZLE.room_B_3)   ? '.': occ.at(&PUZZLE.room_B_3)->type,
                 !occ.count(&PUZZLE.room_B_3)   ? "" : off,

                 !occ.count(&PUZZLE.room_C_3)   ? "" : (
                     occ.at(&PUZZLE.room_C_3)->owns(&PUZZLE.room_C_3) ? red : blue),
                 !occ.count(&PUZZLE.room_C_3)   ? '.': occ.at(&PUZZLE.room_C_3)->type,
                 !occ.count(&PUZZLE.room_C_3)   ? "" : off,

                 !occ.count(&PUZZLE.room_D_3)   ? "" : (
                     occ.at(&PUZZLE.room_D_3)->owns(&PUZZLE.room_D_3) ? red : blue),
                 !occ.count(&PUZZLE.room_D_3)   ? '.': occ.at(&PUZZLE.room_D_3)->type,
                 !occ.count(&PUZZLE.room_D_3)   ? "" : off,

                 !occ.count(&PUZZLE.room_A_2)   ? "" : (
                     occ.at(&PUZZLE.room_A_2)->owns(&PUZZLE.room_A_2) ? red : blue),
                 !occ.count(&PUZZLE.room_A_2)   ? '.': occ.at(&PUZZLE.room_A_2)->type,
                 !occ.count(&PUZZLE.room_A_2)   ? "" : off,

                 !occ.count(&PUZZLE.room_B_2)   ? "" : (
                     occ.at(&PUZZLE.room_B_2)->owns(&PUZZLE.room_B_2) ? red : blue),
                 !occ.count(&PUZZLE.room_B_2)   ? '.': occ.at(&PUZZLE.room_B_2)->type,
                 !occ.count(&PUZZLE.room_B_2)   ? "" : off,

                 !occ.count(&PUZZLE.room_C_2)   ? "" : (
                     occ.at(&PUZZLE.room_C_2)->owns(&PUZZLE.room_C_2) ? red : blue),
                 !occ.count(&PUZZLE.room_C_2)   ? '.': occ.at(&PUZZLE.room_C_2)->type,
                 !occ.count(&PUZZLE.room_C_2)   ? "" : off,

                 !occ.count(&PUZZLE.room_D_2)   ? "" : (
                     occ.at(&PUZZLE.room_D_2)->owns(&PUZZLE.room_D_2) ? red : blue),
                 !occ.count(&PUZZLE.room_D_2)   ? '.': occ.at(&PUZZLE.room_D_2)->type,
                 !occ.count(&PUZZLE.room_D_2)   ? "" : off,

                 !occ.count(&PUZZLE.room_A_1)   ? "" : (
                     occ.at(&PUZZLE.room_A_1)->owns(&PUZZLE.room_A_1) ? red : blue),
                 !occ.count(&PUZZLE.room_A_1)   ? '.': occ.at(&PUZZLE.room_A_1)->type,
                 !occ.count(&PUZZLE.room_A_1)   ? "" : off,

                 !occ.count(&PUZZLE.room_B_1)   ? "" : (
                     occ.at(&PUZZLE.room_B_1)->owns(&PUZZLE.room_B_1) ? red : blue),
                 !occ.count(&PUZZLE.room_B_1)   ? '.': occ.at(&PUZZLE.room_B_1)->type,
                 !occ.count(&PUZZLE.room_B_1)   ? "" : off,

                 !occ.count(&PUZZLE.room_C_1)   ? "" : (
                     occ.at(&PUZZLE.room_C_1)->owns(&PUZZLE.room_C_1) ? red : blue),
                 !occ.count(&PUZZLE.room_C_1)   ? '.': occ.at(&PUZZLE.room_C_1)->type,
                 !occ.count(&PUZZLE.room_C_1)   ? "" : off,

                 !occ.count(&PUZZLE.room_D_1)   ? "" : (
                     occ.at(&PUZZLE.room_D_1)->owns(&PUZZLE.room_D_1) ? red : blue),
                 !occ.count(&PUZZLE.room_D_1)   ? '.': occ.at(&PUZZLE.room_D_1)->type,
                 !occ.count(&PUZZLE.room_D_1)   ? "" : off);
          fflush(stdout);
      }
};

using pstate = std::shared_ptr<const state>;

template<> struct hash<pstate>
{
    auto operator()(const pstate& p) const noexcept
      {
          static const auto hasher = hash<const void*>();
          return accumulate(p->pos.cbegin(), p->pos.cend(), size_t(1481219),
                            [](size_t init, const state::position& p)
                            {
                                return (init << 5) + init  + hasher(p.pod) + hasher(p.node);
                            });
      }
};

template<> struct equal_to<pstate>
{
    bool operator()(const pstate& a, const pstate& b) const noexcept
      {
          return *a == *b;
      }
};

const state FINAL {{state::position{&POD_A, &PUZZLE.room_A_1},
                    state::position{&POD_A, &PUZZLE.room_A_2},
                    state::position{&POD_A, &PUZZLE.room_A_3},
                    state::position{&POD_A, &PUZZLE.room_A_4},
                    state::position{&POD_B, &PUZZLE.room_B_1},
                    state::position{&POD_B, &PUZZLE.room_B_2},
                    state::position{&POD_B, &PUZZLE.room_B_3},
                    state::position{&POD_B, &PUZZLE.room_B_4},
                    state::position{&POD_C, &PUZZLE.room_C_1},
                    state::position{&POD_C, &PUZZLE.room_C_2},
                    state::position{&POD_C, &PUZZLE.room_C_3},
                    state::position{&POD_C, &PUZZLE.room_C_4},
                    state::position{&POD_D, &PUZZLE.room_D_1},
                    state::position{&POD_D, &PUZZLE.room_D_2},
                    state::position{&POD_D, &PUZZLE.room_D_3},
                    state::position{&POD_D, &PUZZLE.room_D_4}}};

pair<vector<pstate>, uint64_t> aye_splat(const state& initial_state)
{
    const auto start = std::make_shared<state>(initial_state);
    unordered_map<pstate, uint64_t> costs {{start, 0}};
    unordered_map<pstate, pstate> parents {{start, start}};
    unordered_set<pstate> livelist {start};
    unordered_set<pstate> deadlist;

    while (!livelist.empty())
    {
        auto n = *min_element(livelist.cbegin(), livelist.cend(),
                              [&costs](const pstate& a, const pstate& b)
                                {
                                    return costs.at(a) < costs.at(b);
                                });
        // printf("==================\n");
        // printf("Cost: %llu\n", costs.at(n));
        // n->display();
        // printf("------------------\n");
        if (*n == FINAL)
        {
            const auto cost = costs.at(n);
            vector<pstate> path;
            while (parents.at(n) != n)
            {
                path.push_back(n);
                n = parents.at(n);
            }
            path.push_back(start);
            reverse(path.begin(), path.end());
            return {path, cost};
        }

        for (const auto& [m, cost]: n->get_moves())
        {
            const auto total_cost = costs.at(n) + cost;
            if (!livelist.count(m) && !deadlist.count(m))
            {
                parents[m] = n;
                costs[m] = total_cost;
                livelist.insert(m);
                // printf("Cost: -> %llu\n", costs.at(m));
                // m->display();
            }
            else if (costs.at(m) > total_cost)
            {
                // printf("Cost: %llu -> %llu\n", costs.at(m), total_cost);
                // m->display();
                costs[m] = total_cost;
                parents[m] = n;
                if (deadlist.count(m))
                {
                    deadlist.erase(m);
                    livelist.insert(m);
                }
            }
         }
        livelist.erase(n);
        deadlist.insert(n);
    }

    return {{}, 0};
}


void solve(const state& initial_state)
{
    initial_state.display();

    const auto [path, cost] = aye_splat(initial_state);
    if (path.empty())
    {
        printf("No path found\n");
        return;
    }

    printf("Cost: %llu\n", cost);
    for (auto it = path.cbegin(); it != path.cend(); ++it)
        (*it)->display();
}

const state EXAMPLE {{state::position{&POD_A, &PUZZLE.room_A_1},
                      state::position{&POD_A, &PUZZLE.room_D_1},
                      state::position{&POD_A, &PUZZLE.room_C_2},
                      state::position{&POD_A, &PUZZLE.room_D_3},
                      state::position{&POD_B, &PUZZLE.room_A_4},
                      state::position{&POD_B, &PUZZLE.room_C_4},
                      state::position{&POD_B, &PUZZLE.room_B_2},
                      state::position{&POD_B, &PUZZLE.room_C_3},
                      state::position{&POD_C, &PUZZLE.room_B_4},
                      state::position{&POD_C, &PUZZLE.room_C_1},
                      state::position{&POD_C, &PUZZLE.room_B_3},
                      state::position{&POD_C, &PUZZLE.room_D_2},
                      state::position{&POD_D, &PUZZLE.room_A_2},
                      state::position{&POD_D, &PUZZLE.room_A_3},
                      state::position{&POD_D, &PUZZLE.room_B_1},
                      state::position{&POD_D, &PUZZLE.room_D_4}}};

const state INPUT {{state::position{&POD_A, &PUZZLE.room_B_1},
                    state::position{&POD_A, &PUZZLE.room_D_4},
                    state::position{&POD_A, &PUZZLE.room_C_2},
                    state::position{&POD_A, &PUZZLE.room_D_3},
                    state::position{&POD_B, &PUZZLE.room_C_1},
                    state::position{&POD_B, &PUZZLE.room_C_4},
                    state::position{&POD_B, &PUZZLE.room_B_2},
                    state::position{&POD_B, &PUZZLE.room_C_3},
                    state::position{&POD_C, &PUZZLE.room_A_1},
                    state::position{&POD_C, &PUZZLE.room_D_1},
                    state::position{&POD_C, &PUZZLE.room_B_3},
                    state::position{&POD_C, &PUZZLE.room_D_2},
                    state::position{&POD_D, &PUZZLE.room_A_2},
                    state::position{&POD_D, &PUZZLE.room_A_3},
                    state::position{&POD_D, &PUZZLE.room_A_4},
                    state::position{&POD_D, &PUZZLE.room_B_4}}};


int main()
{
    // solve(EXAMPLE);
    solve(INPUT);
    return 0;
}
