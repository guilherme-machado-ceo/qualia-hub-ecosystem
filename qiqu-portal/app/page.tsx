import Header from "./components/Header";
import Hero from "./components/Hero";
import Cards from "./components/Cards";
import Roadmap from "./components/Roadmap";
import Footer from "./components/Footer";

export default function Home() {
  return (
    <div className="bg-q-dark">
      <Header />
      <main>
        <Hero />
        <Cards />
        <Roadmap />
      </main>
      <Footer />
    </div>
  );
}