import scene

from components.linear_graph import LinearGraph


class StatisticsScene(scene.Scene):

    def __init__(self, name):
        super().__init__(name)  # スーパークラス Omajinai

        # data
        self.data_x, self.data_y = [], []
        self.label_x, self.label_y = [], []

        self.graph = self.make_graph()
        self.zoom_on = 1.0

    def update(self, pyxel):
        if pyxel.btnp(pyxel.KEY_S):
            self.app.scenes_manager.transition("main_scene")

        wheel_diff = pyxel.mouse_wheel
        if wheel_diff != 0:
            self.zoom_on -= wheel_diff / 10.0
            if self.zoom_on > 1.0:
                self.zoom_on = 1.0
            elif self.zoom_on < 0.05:
                self.zoom_on = 0.05
            self.graph.calculate(zoom=self.zoom_on)  # 再計算

    def draw(self, pyxel):
        self.graph.render(pyxel, x=23, y=130, title="Your Score statics x{}".format(round(self.zoom_on, 1)))
        pyxel.text(5, 190, "Press S to back to main.", 5)

    def before_render(self, pyxel, parameters, before):
        data = self.app.store.records
        data = data[::-1]  # リストを逆順にする
        size = len(data)
        self.data_x = [i for i in range(size)]  # index
        self.data_y = self.label_y = [int(data[i][1]) for i in range(size)]  # score
        self.label_x = [size-i for i in range(size)]  # index
        self.zoom_on = 1.0  # set Default
        self.graph = self.make_graph()
        self.graph.calculate(zoom=self.zoom_on)

    """
        グラフオブジェクトを作成する
        @param app グラフオブジェクトを作成する
    """
    def make_graph(self):
        return LinearGraph(data_x=self.data_x, data_y=self.data_y, label_x=self.label_x, label_y=self.label_y, zoom=0.1, graph_size=[170, 100])
