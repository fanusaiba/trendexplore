import { useState } from "react";
import { motion as Umotion } from "framer-motion";

export default function Test() {
  const [open, setOpen] = useState(false);

  return (
    <motion.div
      onClick={() => setOpen(!open)}
      animate={{ scale: open ? 1.2 : 1 }}
      className="p-4 bg-blue-200 rounded cursor-pointer"
    >
      Click me
    </motion.div>
  );
}
