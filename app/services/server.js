import express from "express";
import cookieParser from "cookie-parser";
import cors from "cors";
import cartRoutes from "./routes/cartRoutes.js";

const app = express();

app.use(cors({ origin: true, credentials: true }));
app.use(express.json());
app.use(cookieParser());

app.use("/carts", cartRoutes);

app.listen(5000, () => {
  console.log("Server running on 5000");
});
