from class_definitions import BoardState, Direction, Nothing, Apple, GameOver, HailVictory
import time
import numpy as np
import json
import sys

global DEBUG
DEBUG = False

def rdir_clr(bs, dir):
    """checks if a relative direction (dir3) is clear"""
    head = bs.snakeblocks[0]
    move = bs.direction_3_to_4(dir)
    move_t = [move.value[0], move.value[1]] #coordinate transforms of the move from param <dir>

    #calculate validity (is it on the map?)
    block_at_future = [head[0]+move_t[0], head[1]+move_t[1]]
    if not (block_at_future[0] >= 0 and block_at_future[0] < bs.x):
        return 0
    if not (block_at_future[1] >= 0 and block_at_future[1] < bs.y):
        return 0
    return isinstance(bs.internal_map[block_at_future[0]][block_at_future[1]], Nothing) or isinstance(bs.internal_map[block_at_future[0]][block_at_future[1]], Apple)

def front_clear(bs):
    return 0+rdir_clr(bs, Direction.FORWARD)*1

def left_clear(bs):
    return 0+rdir_clr(bs, Direction.LEFT)*1

def right_clear(bs):
    return 0+rdir_clr(bs, Direction.RIGHT)*1

def is_apple_in_dir(bs, dir):
    head = bs.snakeblocks[0]
    move = bs.direction_3_to_4(dir)
    move_t = [move.value[0], move.value[1]] #coordinate transforms of the move from param <dir>
    apple_rel = [bs.apple[0]-head[0], bs.apple[1]-head[1]] #relative direction of the apple
    return move_t[0]*apple_rel[0] >= 0 and move_t[1]*apple_rel[1] >= 0

def apple_front(bs):
    return 0+is_apple_in_dir(bs, Direction.FORWARD)*1

def apple_left(bs):
    return 0+is_apple_in_dir(bs, Direction.LEFT)*1

def apple_right(bs):
    return 0+is_apple_in_dir(bs, Direction.RIGHT)*1

class EVO_NN:
    def __init__(self, func_list=[left_clear, front_clear, right_clear, apple_left, apple_front, apple_right], weights=None):
        self.flist = func_list
        self.game = BoardState(x=10, y=10)
        self.lay1 = 32
        self.lay2 = 8
        self.lay3 = 3
        
        if weights is None:
            #weights, adjust so that sum should be ~0.5
            self.l1w = (np.random.rand(self.lay1, len(self.flist)) * 2 - 1) / len(self.flist)
            self.l2w = (np.random.rand(self.lay2, self.lay1) * 2 - 1) / self.lay1
            self.l3w = (np.random.rand(3, self.lay2) * 2 - 1) / self.lay2

            self.l1b = (np.random.rand(self.lay1)) * 2 - 1
            self.l2b = (np.random.rand(self.lay2)) * 2 - 1
            self.l3b = (np.random.rand(self.lay3)) * 2 - 1
        else:
            self.l1w = np.array(weights["l1"])
            self.l2w = np.array(weights["l2"])
            self.l3w = np.array(weights["l3"])

            self.l1b = np.array(weights["b1"])
            self.l2b = np.array(weights["b2"])
            self.l3b = np.array(weights["b3"])

    def eval_nn(self):
        def softmax(z):
            return np.exp(z)/np.sum(np.exp(z))
        def tanh(z):
            return np.tanh(z)
        assert isinstance(self.game, BoardState), "Bad self.game type"
        for f in self.flist:
            assert f.__class__.__name__ == "function", repr(f) + " is not a function"
        self.inputs = np.array([f(self.game) for f in self.flist])
        l1 = tanh(np.matmul(self.l1w, self.inputs) + self.l1b)
        l2 = tanh(np.matmul(self.l2w, l1) + self.l2b)
        l3 = softmax(np.matmul(self.l3w, l2) + self.l3b)

        dir = [Direction.LEFT, Direction.FORWARD, Direction.RIGHT]
        out = [0, 0, 0]
        out[np.argmax(l3)] = 1
        return dir[np.argmax(l3)], out

    def play_game(self):
        score = 0
        moves = 0
        log = "move#: %s, score: %s\n"%(moves, score) + self.game.__str__()
        try:
            for _ in range(100):
                moves += 1
                move_dir, one_hot = self.eval_nn()
                self.game.move3(move_dir)
                last_pos = self.game.last_pos
                head = self.game.snakeblocks[0]
                if (head[0]**2+head[1]**2)-(last_pos[0]**2+last_pos[1]**2) > 0:
                    score += 1
                else:
                    score -= 1.5
                if self.game.touched_apple:
                    score += 50
                log += "move#: %s, score: %s\n"%(moves, score) + self.game.__str__()
        except Exception as e:
            if isinstance(e, HailVictory):
                score += 100000
                return score, moves
            elif isinstance(e, GameOver):
                score -= 10000
                return score, moves
            else:
                raise e
        finally:
            if DEBUG:
                print("Anomaly detected")
                with open("log.txt","w", encoding="utf-8") as f:
                    f.write(log)
                sys.exit(0)
        return score, moves


class GenerationEVO_NN:
    def __init__(self, size=10, load_from_file=None, verbose=True):
        """
        package should be in form:
        {
            history = {
                g1 = list of [score, steps]
                g2 = ..
                gn = ..
            }
            top = list of dictionaries {result:[score, steps], weights:{l1:..., l2:..., l3:...}}
        }
        """
        if load_from_file is None:
            print("Initializing new generation...")
            self.generation = 0
            self.size = size
            self.Internal_NNs = [EVO_NN() for _ in range(size)]
            self.results = []
            self.history = {}
            self.top_generation = []
            #list of dicts: {results: [score, steps], weights: {l1:..., l2:..., l3:...}}
            self.evaluate_weights(display=verbose)
        else:
            with open(load_from_file, encoding="utf-8") as f:
                print("Loading generation from file...")
                package = json.load(f)
                self.history = package["history"]
                self.results = []
                self.top_generation = package["top"]
                self.generation = len(self.history)-1
                self.size = len(self.history["g0"])
                self.Internal_NNs = [EVO_NN(weights=i["weights"]) for i in self.top_generation]
                print("Generation data loaded. Total of %s generations found."%(self.generation+1))
    def evaluate_weights(self, display=True):
        self.results = []
        for i in self.Internal_NNs:
            result = i.play_game()
            self.results.append(result)
            if len(self.top_generation) < self.size:
                weights = {}
                weights["l1"] = i.l1w.tolist()
                weights["l2"] = i.l2w.tolist()
                weights["l3"] = i.l3w.tolist()
                weights["b1"] = i.l1b.tolist()
                weights["b2"] = i.l2b.tolist()
                weights["b3"] = i.l3b.tolist()
                self.top_generation.append({"result":result, "weights":weights})
            else:
                top_scores = [x["result"][0] for x in self.top_generation]
                min_score = min(top_scores)
                if result[0] > min_score:
                    weights = {}
                    weights["l1"] = i.l1w.tolist()
                    weights["l2"] = i.l2w.tolist()
                    weights["l3"] = i.l3w.tolist()
                    weights["b1"] = i.l1b.tolist()
                    weights["b2"] = i.l2b.tolist()
                    weights["b3"] = i.l3b.tolist()
                    idx = np.argmin(top_scores)
                    self.top_generation[idx] = {"result":result, "weights":weights}
        if display:
            print("GENERATION %s"%(self.generation+1))
            print(self.results)
            top_scores = [x["result"][0] for x in self.top_generation]
            print("TOP:",top_scores)
    def retrieve_weights(self):
        gstring = "g"+str(self.generation)
        self.history[gstring] = None
        self.history[gstring] = []
        if False: #disable weight saving
            for nn in self.Internal_NNs:
                weights = {}
                weights["l1"] = nn.l1w.tolist()
                weights["l2"] = nn.l2w.tolist()
                weights["l3"] = nn.l3w.tolist()
                weights["b1"] = nn.l1b.tolist()
                weights["b2"] = nn.l2b.tolist()
                weights["b3"] = nn.l3b.tolist()
            self.history[gstring].append(weights)
        weights = {}
        weights["top"] = self.top_generation
        self.history[gstring] = self.results
    def save_weights(self, filename="history.json"):
        self.retrieve_weights()
        with open(filename,"w", encoding="utf-8") as f:
            json.dump({"history":self.history, "top":self.top_generation}, f)
    def evolve(self, ptile = 80, evolution_wildness=0.05):
        def randomize_percent(arr, p):
            out = arr * np.reshape(np.random.rand(len(np.ravel(arr))),(np.shape(arr))) * 2 * p + 1 - p
            return out
        def randomize_flat(arr, max_amt):
            out = arr + (np.reshape(np.random.rand(len(np.ravel(arr))),(np.shape(arr))) * 2 - 1) * max_amt
            return out
        scores = [x[0] for x in self.results]
        cutoff = np.percentile(scores, ptile)
        indices = np.where(scores > cutoff)
        new_net = []
        assert len(self.top_generation) > 0, "Top generation is empty"
        for _ in range(self.size):
            idx = np.random.randint(len(indices))
            victorious_network = self.top_generation[idx]["weights"]
            weights = {}
            weights["l1"] = randomize_flat(victorious_network["l1"], evolution_wildness)
            weights["l2"] = randomize_flat(victorious_network["l2"], evolution_wildness)
            weights["l3"] = randomize_flat(victorious_network["l3"], evolution_wildness)
            weights["b1"] = randomize_flat(victorious_network["b1"], evolution_wildness)
            weights["b2"] = randomize_flat(victorious_network["b2"], evolution_wildness)
            weights["b3"] = randomize_flat(victorious_network["b3"], evolution_wildness)

            new_net.append(EVO_NN(weights=weights))
        self.generation += 1
        self.Internal_NNs = new_net

start = time.time()

#start#
g = GenerationEVO_NN(load_from_file="history.json")
g.save_weights("history.json")
for i in range(500):
    g.evaluate_weights(display=True)
    g.save_weights("history.json")
    g.evolve(evolution_wildness=0.1)
#end#

end = time.time()
print("Seconds elapsed:", end-start)